# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from ..azure_common import BaseTest


class VMSnapshotTest(BaseTest):
    def test_azure_vm_snapshot_schema_validate(self):
        p = self.load_policy({
            'name': 'test-vm-snapshot',
            'resource': 'azure.vm-snapshot'
        }, validate=True)
        self.assertTrue(p)

    def test_find_by_name(self):
        p = self.load_policy({
            'name': 'test-azure-vm-snapshot',
            'resource': 'azure.vm-snapshot',
            'filters': [
                {'type': 'value',
                 'key': 'name',
                 'op': 'glob',
                 'value_type': 'normalize',
                 'value': 'cc*'}],
        })
        resources = p.run()
        self.assertEqual(len(resources), 1)
