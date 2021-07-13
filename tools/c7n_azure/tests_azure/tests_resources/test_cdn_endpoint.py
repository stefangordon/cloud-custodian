# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from ..azure_common import BaseTest


class CdnEndpointTest(BaseTest):
    def test_azure_cdn_endpoint_schema_validate(self):
        p = self.load_policy({
            'name': 'test-cdn-endpoint',
            'resource': 'azure.cdn-endpoint'
        }, validate=True)
        self.assertTrue(p)

    def test_find_by_name(self):
        p = self.load_policy({
            'name': 'test-azure-cdn-endpoint',
            'resource': 'azure.cdn-endpoint',
            'filters': [
                {'type': 'value',
                 'key': 'name',
                 'op': 'glob',
                 'value_type': 'normalize',
                 'value': 'cc*'}],
        })
        resources = p.run()
        self.assertEqual(len(resources), 1)
