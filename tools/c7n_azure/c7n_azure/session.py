# Copyright 2018 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import os
from azure.cli.core.cloud import AZURE_PUBLIC_CLOUD
from azure.cli.core._profile import Profile
from azure.common.credentials import ServicePrincipalCredentials

class Session(object):

    def __init__(self):
        env_variables = ['AZURE_TENANT_ID', 'AZURE_SUBSCRIPTION_ID', 'AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET']

        if all(k in env_variables for k in os.environ):
            # Set credentials with environment variables
            self.credentials = ServicePrincipalCredentials(
                client_id=os.environ['AZURE_CLIENT_ID'],
                secret=os.environ['AZURE_CLIENT_SECRET'],
                tenant=os.environ['AZURE_TENANT_ID']
            )
            self.subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
            self.tenant_id = os.environ['AZURE_TENANT_ID']
            pass
        else:
            # Try to set credentials with Azure CLI
            (self.credentials,
             self.subscription_id,
             self.tenant_id) = Profile().get_login_credentials(
                resource=AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id)

        self.__provider_cache = {}

    def client(self, client):
        service_name, client_name = client.rsplit('.', 1)
        svc_module = importlib.import_module(service_name)
        klass = getattr(svc_module, client_name)
        return klass(self.credentials, self.subscription_id)

    def resource_api_version(self, resource):
        """ latest non-preview api version for resource """
        if resource.type in self.__provider_cache:
            return self.__provider_cache[resource.type]

        namespace = resource.id.split('/')[6]
        resource_client = self.client('azure.mgmt.resource.ResourceManagementClient')
        provider = resource_client.providers.get(namespace)

        rt = next((t for t in provider.resource_types if t.resource_type == str(resource.type).split('/')[-1]), None)
        if rt and rt.api_versions:
            versions = [v for v in rt.api_versions if 'preview' not in v.lower()]
            api_version = versions[0] if versions else rt.api_versions[0]
            self.__provider_cache[resource.type] = api_version
            return api_version
