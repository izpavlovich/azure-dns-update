from time import gmtime, strftime
from dns import resolver
from azure.mgmt.dns import DnsManagementClient
from azure.common.credentials import ServicePrincipalCredentials

from config import Config

# Goggle DNS Server (needed to determine current ip address)
resolver.nameservers = ['8.8.8.8']

ips = resolver.query(Config['host'], 'A')
ips2 = resolver.query('o-o.myaddr.l.google.com', 'TXT')

record = ips[0].address
current = ips2[0].strings[0].decode('UTF-8')

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