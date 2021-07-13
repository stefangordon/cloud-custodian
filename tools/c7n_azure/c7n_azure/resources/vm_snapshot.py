# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n_azure.resources.arm import ArmResourceManager
from c7n_azure.provider import resources


@resources.register('vm-snapshot')
class VMSnapshot(ArmResourceManager):
    """V MSnapshot Resource

    :example:

    This policy will find all V MSnapshot instances.

    .. code-block:: yaml

        policies:
          - name: all-vm-snapshot-resources
            resource: azure.vm-snapshot
    """

    class resource_type(ArmResourceManager.resource_type):
        doc_groups = ['Network']

        service = 'azure.mgmt.vmsnapshot'
        client = 'VMSnapshotManagementClient'
        enum_spec = ('VMSnapshot', 'list', None)
        default_report_fields = (
            'name',
            'location',
            'resourceGroup'
        )
        resource_type = 'Microsoft.Compute/snapshots'
