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

import six
from c7n_azure.query import QueryResourceManager, QueryMeta
from c7n_azure.actions import Tag
from c7n_azure.utils import ResourceIdParser


class ArmResourceQueryMeta(QueryMeta):
    """metaclass to add actions/filters common for ARM resources."""
    def __new__(cls, name, parents, attrs):
        query_meta = super(ArmResourceQueryMeta, cls).__new__(cls, name, parents, attrs)
        if hasattr(query_meta, 'action_registry'):
            query_meta.action_registry.register('tag', Tag)
        return query_meta


@six.add_metaclass(ArmResourceQueryMeta)
class ArmResourceManager(QueryResourceManager):

    def augment(self, resources):
        for resource in resources:
            if 'id' in resource:
                resource['resourceGroup'] = ResourceIdParser.get_resource_group(resource['id'])
        return resources
