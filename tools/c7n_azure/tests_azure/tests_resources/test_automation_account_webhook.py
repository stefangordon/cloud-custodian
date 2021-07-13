# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from ..azure_common import BaseTest


class AutomationAccountWebhookTest(BaseTest):
    def test_azure_automation_account_webhook_schema_validate(self):
        p = self.load_policy({
            'name': 'test-automation-account-webhook',
            'resource': 'azure.automation-account-webhook'
        }, validate=True)
        self.assertTrue(p)

    def test_find_by_name(self):
        p = self.load_policy({
            'name': 'test-azure-automation-account-webhook',
            'resource': 'azure.automation-account-webhook',
            'filters': [
                {'type': 'value',
                 'key': 'name',
                 'op': 'glob',
                 'value_type': 'normalize',
                 'value': 'cc*'}],
        })
        resources = p.run()
        self.assertEqual(len(resources), 1)
