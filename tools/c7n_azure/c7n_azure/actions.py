# Copyright 2015-2017 Capital One Services, LLC
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
"""
Actions to take on Azure resources
"""
from c7n.actions import BaseAction
from c7n import utils
from azure.mgmt.resource import ResourceManagementClient


class Tag(BaseAction):
    """
    Add a tag to any Azure resource
    """

    schema = utils.type_schema(
        'tag',
        required=['tag'],
        **{
            'tag': {'type': 'string'},
            'value': {'type': 'string'}
        }
    )

    def validate(self):
        # All Azure resource should support add tags
        return self

    def process(self, resources):
        pass
