# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from ..azure_common import BaseTest


class ServiceBusTest(BaseTest):
    def test_azure_service_bus_schema_validate(self):
        p = self.load_policy({
            'name': 'test-service-bus',
            'resource': 'azure.service-bus'
        }, validate=True)
        self.assertTrue(p)

    def test_find_by_name(self):
        p = self.load_policy({
            'name': 'test-azure-service-bus',
            'resource': 'azure.service-bus',
            'filters': [
                {'type': 'value',
                 'key': 'name',
                 'op': 'glob',
                 'value_type': 'normalize',
                 'value': 'cc*'}],
        })
        resources = p.run()
        self.assertEqual(len(resources), 1)
