#!/usr/bin/python3
import json
import requests
from requests import urllib3
import time
import pprint as pp
import csv
import pandas as pd
from docx import Document
from docx.shared import Inches
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
    def get_network_info(append_url = '', dict_key =''):
        data = http_get(meraki_url='networks/{}/{}'.format(network["id"],
        append_url))
        for i in data:
            meraki_data[dict_key].append(data)
    get_network_info(append_url='devices', dict_key='devices')
    get_network_info(append_url='securityEvents', dict_key='securityEvents')
    get_network_info(append_url='ssids', dict_key='ssids')
    get_network_info(append_url='firewalledServices', dict_key='fwServices')
    get_network_info(append_url='l3FirewallRules', dict_key='l3FirewallRules')
    get_network_info(append_url='vlans', dict_key='vlans')


licenses_df = pd.DataFrame.from_dict(meraki_data['licenses'])
orgs_df = pd.DataFrame.from_dict(meraki_data['orgs'])
networks_df = pd.DataFrame.from_dict(meraki_data['networks'])
meraki_vlans_df = pd.DataFrame.from_dict(meraki_data['vlans'])
l3FirewallRules_df = pd.DataFrame.from_dict(meraki_data['l3FirewallRules'])
ssids_df = pd.DataFrame.from_dict(meraki_data['ssids'])
devices_df = pd.DataFrame.from_dict(meraki_data['devices'])
#print (meraki_data_df)

with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
    licenses_df.to_excel(writer, sheet_name='licenses')
    meraki_vlans_df.to_excel(writer, sheet_name='VLANs')
    l3FirewallRules_df.to_excel(writer, sheet_name='l3FirewallRules')
    devices_df.to_excel(writer, sheet_name='devices')
    l3FirewallRules_df.to_excel(writer, sheet_name='l3FirewallRules')
    ssids_df.to_excel(writer, sheet_name='ssids')
