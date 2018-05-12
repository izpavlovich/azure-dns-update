# Script to dynamically update Azure DNS records based on current IP address

When deployed and scheduled to run periodically this script will update DNS Record in Azure DNS zone providing functionality similar to Dynamic DNS.

## How it works

The script will query to OpenDNS to receive the current IP address of the inquiring host [[More about that](https://code.blogs.iiidefix.net/posts/get-public-ip-using-dns/)]. Provided information will be compared with the DNS response for the host. If the two values are not equal, the script will invoke call to azure to update DNS record with the current IP.

## Prerequisites

To make this work the following is needed

1. Azure Subscription
1. [Azure DNS Zone](https://docs.microsoft.com/en-us/azure/dns/dns-getstarted-portal)
1. [Service Principal](https://aka.ms/Wqyng5) (Azure service account that will perform the update)
1. Client machine with installed Python and PIP

## How to use it

### Clone the repository and install requirements in a virtual environment

```bash
git clone https://github.com/izpavlovich/azure-dns-update.git
cd azure-dns-update
pip install -r requirements.txt virtualenv
```

### Edit config.py file to

```python
Config = {
    # Azure Credentials
    # This example uses [Service Principal](https://aka.ms/Wqyng5) for Azure access
    'clientId': '<Service Principal ID>',
    'secret': '<Service Principal Password>',
    'tenant': '<Service Principal Tenant>',
    'subscriptionId': '<You subscription id>',
    # Dns params
    'resourceGroup': '',
    'zoneName': '<Name of the Azure Zone>',
    # The value of the actual DNS record
    # Use @ for root or other value for a subdomain
    'recordSetName': '@',
    # Host name that needs to be checked
    'host': 'something.yours.com'
}
```

### Run the script

```bash
py azure-dns-update.py
```

or, you can set up [cron to run it periodically](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/).

## Considerations

- When creating a service principal, it is more secure scope the permission only the the DNS Zone you will be updating. In this case, if your secret is compromised it could only be used to change the zone resource.
- When creating DNS Record, set up TTL (time to live) low. 60 seconds to 5 minutes is a good range. If you are running the script on the schedule, match the TTL parameter to your schedule interval.
