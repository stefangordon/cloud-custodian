# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n_azure.resources.arm import ArmResourceManager
from c7n_azure.provider import resources


@resources.register('service-bus')
class ServiceBus(ArmResourceManager):
    """Service Bus Resource

    :example:

    This policy will find all Service Bus instances.

    .. code-block:: yaml

        policies:
          - name: all-service-bus-resources
            resource: azure.service-bus
    """

    class resource_type(ArmResourceManager.resource_type):
        doc_groups = ['Network']

        service = 'azure.mgmt.servicebus'
        client = 'ServiceBusManagementClient'
        enum_spec = ('ServiceBus', 'list', None)
        default_report_fields = (
            'name',
            'location',
            'resourceGroup'
        )
        resource_type = 'Microsoft.ServiceBus/namespaces'
