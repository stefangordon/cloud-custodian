Find Open SSH Ports
===================

This policy will deny access to all security rules with Inbound SSH ports in the range [8080,8090]

.. code-block:: yaml

     policies:
       - name: open-ingress
         resource: azure.networksecuritygroup
         filters:
          - type: ingress
            FromPort: 8080
            ToPort: 8090
         actions:
          - type: close

Available types:
    - ingress - Inbound Security Rules
    - egress - Outbound Security Rules

Available filters:
    - FromPort - Lower bound of port range (inclusive and can be used alone to indicate all ports at or above number)
    - ToPort - Upper bound of port range (inclusive and can be used alone to indicate all ports at or below number)
    - Ports - Filter on ports contained in list.  Ex: Ports [8080,8081]
    - OnlyPorts - Filter on ports NOT contained in list. Ex: OnlyPorts [22] 
    - IpProtocol - [TCP,UDP] - Specify for rules with indicated protocol