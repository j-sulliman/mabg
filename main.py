#!/usr/bin/python3
import json
import requests
from requests import urllib3
import time
import pprint as pp
import csv
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_get(meraki_url):
    base_url = ('https://api.meraki.com/api/v0/{}'.format(meraki_url))
    headers = {'X-Cisco-Meraki-API-Key': '029c931f51ee7ea3d74de7cbf6e2db80b17d38d7'}
    get_response = requests.get(base_url, headers=headers, verify=False).json()
    time.sleep(0.5)
    return get_response

# Intitialise dictionary to store returned data
meraki_data = {}
orgs = http_get(meraki_url='organizations')
meraki_data['orgs'] = orgs
meraki_data["networks"] = []
meraki_data["licenses"] = []
meraki_data["devices"] = []
meraki_data["securityEvents"] = []
meraki_data["ssids"] = []
meraki_data["fwServices"] = []
meraki_data["intrusionPrevention"] = []
meraki_data["malwareSettings"] = []
meraki_data["l3FirewallRules"] = []
meraki_data["vlans"] = []


for org in meraki_data['orgs']:
    # Get networks from all orgs and add to dictionary
    networks = http_get(meraki_url='organizations/{}/networks'.format(org["id"]))
    for network in networks:
        meraki_data["networks"].append(network)

    # Get license info from all orgs and add to dictionary
    licenses = http_get(meraki_url='organizations/{}/licenseState'.format(org["id"]))
    meraki_data["licenses"].append(licenses)

    # Get IPs
    ips = http_get(meraki_url='organizations/{}/security/intrusionSettings'.format(org["id"]))
    for ip in ips:
        meraki_data["intrusionPrevention"].append(ip)

for network in meraki_data['networks']:
    # Get Meraki devices
    devices = http_get(meraki_url='networks/{}/devices'.format(network["id"]))
    for device in devices:
        meraki_data["devices"].append(device)

    # Get Security Events
    sec_events = http_get(meraki_url='networks/{}/securityEvents'.format(network["id"]))
    for sec_event in sec_events:
        meraki_data["securityEvents"].append(sec_event)

    # Get SSIDs
    ssids = http_get(meraki_url='networks/{}/ssids'.format(network["id"]))
    for ssid in ssids:
        meraki_data["ssids"].append(ssid)

    # Get Firewall Services
    fw_services = http_get(meraki_url='networks/{}/firewalledServices'.format(network["id"]))
    for fwService in fw_services:
        meraki_data["fwServices"].append(fwService)

    # Get Malware Settings
    '''
    malware_settings = http_get(meraki_url='networks/{}/malwareSettings'.format(network["id"]))
    for malware in malware_settings:
        meraki_data["malwareSettings"].append(malware)
    '''
    # Get L3 Firewall Rules
    l3_rules = http_get(meraki_url='networks/{}/l3FirewallRules'.format(network["id"]))
    for rule in l3_rules:
        meraki_data["l3FirewallRules"].append(rule)

    # Get VLANs
    vlans = http_get(meraki_url='networks/{}/vlans'.format(network["id"]))
    for vlan in vlans:
        meraki_data["vlans"].append(vlan)


#pp.pprint(meraki_data)

'''
w = csv.writer(open("vlans_output.csv", "w"))
for i in meraki_data['vlans']:
    for key, val in i.items():
        w.writerow([key, val])
'''
licenses_df = pd.DataFrame.from_dict(meraki_data['licenses'])
orgs_df = pd.DataFrame.from_dict(meraki_data['orgs'])
networks_df = pd.DataFrame.from_dict(meraki_data['networks'])
meraki_vlans_df = pd.DataFrame.from_dict(meraki_data['vlans'])
l3FirewallRules_df = pd.DataFrame.from_dict(meraki_data['l3FirewallRules'])
ssids_df = pd.DataFrame.from_dict(meraki_data['ssids'])
devices_df = pd.DataFrame.from_dict(meraki_data['devices'])
#print (meraki_data_df)

with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
    meraki_vlans_df.to_excel(writer, sheet_name='VLANs')
    l3FirewallRules_df.to_excel(writer, sheet_name='l3FirewallRules')
    ssids_df.to_excel(writer, sheet_name='ssids')
...     #df2.to_excel(writer, sheet_name='Sheet_name_2')
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
