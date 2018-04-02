# Copyright 2015-2018 Capital One Services, LLC
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
from __future__ import absolute_import, division, print_function, unicode_literals
from .common import BaseTest
from c7n_azure.session import Session


class SessionTest(BaseTest):
    def setUp(self):
        super(SessionTest, self).setUp()
        session = Session()

    def test_client(self):
        """Simple example showing a VCR recorded test working"""
        s = Session()
        client = s.client('azure.mgmt.resource.ResourceManagementClient')
        #assertIsNotNone(client)
        #resource_group_params = {'location': 'westus'}
        #resource_group_params.update(tags={'hello': 'world'})

        #for item in client.resources.list():
        #    print(s.resource_api_version(item))

