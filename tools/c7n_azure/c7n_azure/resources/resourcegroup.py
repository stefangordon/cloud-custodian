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

from c7n_azure.query import QueryResourceManager
from c7n_azure.provider import resources
from c7n.filters import (
    FilterRegistry, Filter
)
from c7n import utils

filters = FilterRegistry('ec2.filters')

@resources.register('resourcegroup')
class ResourceGroup(QueryResourceManager):

    class resource_type(object):
        service = 'azure.mgmt.resource'
        client = 'ResourceManagementClient'
        enum_spec = ('resource_groups', 'list')

    filter_registry = filters

    @filters.register('empty-group')
    class EmptyGroup(Filter):
        # policies:
        #   - name: test - azure
        #   resource: azure.resourcegroup
        #   filters:
        #       - type: empty - group

        def __call__(self, group):
            client = utils.local_session(self.manager.session_factory).client('azure.mgmt.resource.ResourceManagementClient')
            resources_iterator = client.resources.list_by_resource_group(group['name'])
            return any(True for _ in resources_iterator)

