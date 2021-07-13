# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from ..azure_common import BaseTest


class LogAnalyticsWorkspaceTest(BaseTest):
    def test_azure_log_analytics_workspace_schema_validate(self):
        p = self.load_policy({
            'name': 'test-log-analytics-workspace',
            'resource': 'azure.log-analytics-workspace'
        }, validate=True)
        self.assertTrue(p)

    def test_find_by_name(self):
        p = self.load_policy({
            'name': 'test-azure-log-analytics-workspace',
            'resource': 'azure.log-analytics-workspace',
            'filters': [
                {'type': 'value',
                 'key': 'name',
                 'op': 'glob',
                 'value_type': 'normalize',
                 'value': 'cc*'}],
        })
        resources = p.run()
        self.assertEqual(len(resources), 1)
