import json
import requests
from requests import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_get(meraki_url):
    base_url = ('https://api.meraki.com/api/v0/{}'.format(meraki_url))
    headers = {'X-Cisco-Meraki-API-Key': '029c931f51ee7ea3d74de7cbf6e2db80b17d38d7'}
    get_response = requests.get(base_url, headers=headers, verify=False).json()
    #json_data = json.dumps(get_response)
    return get_response

# Intitialise dictionary to store returned data
meraki_data = {}
orgs = http_get(meraki_url='organizations')
meraki_data['orgs'] = orgs
meraki_data["networks"] = []
meraki_data["licenses"] = []


for org in meraki_data['orgs']:
    # Get networks from all orgs and add to dictionary
    networks = http_get(meraki_url='organizations/{}/networks'.format(org["id"]))
    for network in networks:
        meraki_data["networks"].append(network)

    # Get license info from all orgs and add to dictionary
    licenses = http_get(meraki_url='organizations/{}/licenseState'.format(org["id"]))
    meraki_data["licenses"].append(licenses)
    print(licenses)
    #for license in licenses:

print(meraki_data)


'''
print(orgs[0]["id"])
networks = aci_get(apic_url='organizations/{}/networks'.format(orgs[0]["id"]))
org_license = aci_get(apic_url='organizations/{}/licenseState'.format(orgs[0]["id"]))
print(org_license)
print(networks)
devices = aci_get(apic_url='networks/{}/devices'.format(networks[0]["id"]))
sec_events = aci_get(apic_url='networks/{}/securityEvents'.format(networks[0]["id"]))
ssids = aci_get(apic_url='networks/{}/ssids'.format(networks[0]["id"]))
print(ssids)

print(devices)
firewall_services = aci_get(apic_url='networks/{}/firewalledServices'.format(networks[0]["id"]))
ips = aci_get(apic_url='networks/{}/security/intrusionSettings'.format(networks[0]["id"]))
malware = aci_get(apic_url='networks/{}/security/malwareSettings'.format(networks[0]["id"]))
net_fw = aci_get(apic_url='networks/{}/l3FirewallRules'.format(networks[0]["id"]))
net_vlans = aci_get(apic_url='networks/{}/vlans'.format(networks[0]["id"]))
print(net_vlans)
input('vl??')
print(net_fw)
print(malware)
print(ips)
print(firewall_services)
device_serials = []
for device in devices:
    device_serials.append(device["serial"])
    print(device["serial"])
    input("cio?")
    #switchports = aci_get(apic_url='/devices/{}/switchPorts'.format(device["serial"]))
    #print(switchports)
print(device_serials)

uplinks = []
clients = []

org_ips = aci_get(apic_url='organizations/{}/security/intrusionSettings'.format(orgs[0]["id"]))
print(org_ips)
for serial in device_serials:
    uplink = aci_get(apic_url='networks/{}/devices/{}/uplink'.format(networks[0]["id"], serial))
    uplinks.append({serial : uplink})
    client = aci_get(apic_url='/devices/{}/clients'.format(serial))
'''
'''
    for i in client:
        traffic = aci_get(apic_url='networks/{}/clients/{}/trafficHistory'.format(networks[0]["id"], i["id"]))
        time.sleep(1)
        print(traffic)
    clients.append({'serial_number' : serial,
                    'network_id' : networks[0]["id"],
                    'client_id': client})
'''
