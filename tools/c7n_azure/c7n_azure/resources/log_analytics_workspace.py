# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n_azure.resources.arm import ArmResourceManager
from c7n_azure.provider import resources


@resources.register('log-analytics-workspace')
class LogAnalyticsWorkspace(ArmResourceManager):
    """Log Analytics Workspace Resource

    :example:

    This policy will find all Log Analytics Workspace instances.

    .. code-block:: yaml

        policies:
          - name: all-log-analytics-workspace-resources
            resource: azure.log-analytics-workspace
    """

    class resource_type(ArmResourceManager.resource_type):
        doc_groups = ['Network']

        service = 'azure.mgmt.loganalyticsworkspace'
        client = 'LogAnalyticsWorkspaceManagementClient'
        enum_spec = ('LogAnalyticsWorkspace', 'list', None)
        default_report_fields = (
            'name',
            'location',
            'resourceGroup'
        )
        resource_type = 'Microsoft.OperationalInsights/workspaces'
