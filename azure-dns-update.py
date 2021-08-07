from time import gmtime, strftime
from dns import resolver
from azure.mgmt.dns import DnsManagementClient
from azure.identity import ClientSecretCredential

from config import Config

r= resolver.Resolver(configure=False)
# OpenDNS Servers (needed to determine current ip address)
r.nameservers = ['208.67.222.222', '208.67.220.220']
ips = r.resolve(Config['host'], lifetime=30)
ips2 = r.resolve('myip.opendns.com', lifetime=30)

record = ips[0].address
current = ips2[0].address

if record != current:
    credentials = ClientSecretCredential(
        client_id=Config['clientId'],
        client_secret=Config['secret'],
        tenant_id=Config['tenant']
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