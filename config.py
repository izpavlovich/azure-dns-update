Config = {
    # Azure Credentials
    # This example uses Service Principal to Authentificate
    # Visit: https://aka.ms/Wqyng5
    'clientId': '<Service Principal ID>',
    'secret': '<Service Principal Password>',
    'tenant': '<Service Principal Tenant>',
    'subscriptionId': '<You subscription id>',
    # Dns params
    'resourceGroup': '<The name of a resource group containing the DNS Zone>',
    'zoneName': '<Name of the Azure Zone>',
    # The value of the actual DNS record
    # Use @ for root or other value for a subdomain
    'recordSetName': '@',
    # Host name that needs to be checked
    'host': 'something.yours.com'
}
