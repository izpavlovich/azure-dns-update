from time import gmtime, strftime
from dns import resolver
from azure.mgmt.dns import DnsManagementClient
from azure.common.credentials import ServicePrincipalCredentials

from config import Config

r= resolver.Resolver(configure=False)
# OpenDNS Servers (needed to determine current ip address)
r.nameservers = ['208.67.222.222', '208.67.220.220']
ips = r.query(Config['host'])
ips2 = r.query('myip.opendns.com')

record = ips[0].address
current = ips2[0].address

if record != current:
    credentials = ServicePrincipalCredentials(
        client_id=Config['clientId'],
        secret=Config['secret'],
        tenant=Config['tenant']
    )

    dns_client = DnsManagementClient(
        credentials,
        Config['subscriptionId']
    )

    dns_client.record_sets.create_or_update(
        Config['resourceGroup'],
        Config['zoneName'],
        Config['recordSetName'],
        'A',
        {
            'ttl': 60,
            'arecords': [
                {
                    "ipv4_address": current
                }
            ]
        }
    )

    ts = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    print(ts + ' Record updated to: ' + current)