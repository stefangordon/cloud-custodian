# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from ..azure_common import BaseTest


class ApplicationGatewayTest(BaseTest):
    def setUp(self):
        super(ApplicationGatewayTest, self).setUp()

    def test_app_gateway_validate(self):
        with self.sign_out_patch():
            p = self.load_policy({
                'name': 'test-app-gateway',
                'resource': 'azure.application-gateway'
            }, validate=True)
            self.assertTrue(p)

    def test_find_by_name(self):
        p = self.load_policy({
            'name': 'test-app-gateway',
            'resource': 'azure.application-gateway',
            'filters': [
                {'type': 'value',
                 'key': 'name',
                 'op': 'glob',
                 'value_type': 'normalize',
                 'value': 'ccgateway*'}],
        })
        resources = p.run()
        self.assertEqual(len(resources), 1)
