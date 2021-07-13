# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n_azure.resources.arm import ArmResourceManager
from c7n_azure.provider import resources


@resources.register('automation-account-webhook')
class AutomationAccountWebhook(ArmResourceManager):
    """Automation Account Webhook Resource

    :example:

    This policy will find all Automation Account Webhook instances.

    .. code-block:: yaml

        policies:
          - name: all-automation-account-webhook-resources
            resource: azure.automation-account-webhook
    """

    class resource_type(ArmResourceManager.resource_type):
        doc_groups = ['Network']

        service = 'azure.mgmt.automationaccountwebhook'
        client = 'AutomationAccountWebhookManagementClient'
        enum_spec = ('AutomationAccountWebhook', 'list', None)
        default_report_fields = (
            'name',
            'location',
            'resourceGroup'
        )
        resource_type = 'Microsoft.Automation/automationAccounts/webhooks'
