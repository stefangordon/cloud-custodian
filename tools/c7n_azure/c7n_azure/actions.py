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
from c7n.filters import FilterValidationError


class Tag(BaseAction):
    """
    Add a tag to any Azure resource
    """

    schema = utils.type_schema(
        'tag',
        **{
            'tag': {'type': 'string'},
            'value': {'type': 'string'},
            'tags': {'type': 'object'}
        }
    )

    def validate(self):
        if self.data.get('tags') and self.data.get('tag'):
            raise FilterValidationError(
                "Can't specify both tags and tag, choose one")
        return self

    def process(self, resources):
        session = utils.local_session(self.manager.session_factory)
        client = session.client('azure.mgmt.resource.ResourceManagementClient')

        for resource in resources:
            model = resource.azure_model
            api_version = session.resource_api_version(model)

            tag = self.data.get('tag')
            value = self.data.get('value')

            tags = self.data.get('tags') or model.tags

            if tag and value:
                tags[tag] = value

            model.tags = tags
            client.resources.create_or_update_by_id(model.id, api_version, model)
