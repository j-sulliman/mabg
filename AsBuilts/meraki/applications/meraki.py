#!/usr/bin/python3
import json
import requests
from requests import urllib3
import time
import pprint as pp
import csv
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.section import WD_ORIENT, WD_SECTION
from ..models import MerakiInfo
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def http_get(meraki_url):
    base_url = ('https://api.meraki.com/api/v0/{}'.format(meraki_url))
    for api in MerakiInfo.objects.all():
        api_key = api.api_key
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    try:
        get_response = requests.get(base_url, headers=headers, verify=False)
        status = get_response.status_code
        get_response = get_response.json()
        time.sleep(0.5)
    except:
        print('Meraki Cloud not reachable - check connection')
        get_response = 'unreachable'
        status = 'unreachable'
    return get_response, status


def create_word_doc_title():
    doc = Document('media/Meraki As Built.docx')
    #doc.add_heading(doc_title, 0)
    #doc.add_picture('meraki_splash.png', width=Inches(3.25))
    doc.add_page_break()

    return doc


def create_word_doc_paragraph(doc, heading_text = '', heading_level = 1,
                            paragraph_text = ''):
    doc.add_heading(heading_text, level=heading_level)
    #new_section.orientation = WD_ORIENT.LANDSCAPE
    p = doc.add_paragraph(paragraph_text)

    return doc

def create_word_doc_bullet(
    doc,
    bp1 = '',
    bp2 = '',
    bp3 = '',
    bp4 = '',
    bp5 = ''
    ):
    if bp1 != '':
        doc.add_paragraph(
            bp1, style='List Paragraph'
        )
    if bp2 != '':
        doc.add_paragraph(
            bp2, style='List Paragraph'
        )
    if bp3 != '':
        doc.add_paragraph(
            bp3, style='List Paragraph'
        )
    if bp4 != '':
        doc.add_paragraph(
            bp4, style='List Paragraph'
        )
    if bp5 != '':
        doc.add_paragraph(
            bp5, style='List Paragraph'
        )


    return doc


def create_word_doc_table(doc, df):
    # add a table to the end and create a reference variable
    # extra row is so we can add the header row
    try:
        t = doc.add_table(df.shape[0]+1, df.shape[1], style = 'Grid Table 4 Accent 6')

        # add the header rows.
        for j in range(df.shape[-1]):
            t.cell(0,j).text = df.columns[j]



        # add the rest of the data frame
        for i in range(df.shape[0]):
            for j in range(df.shape[-1]):
                t.cell(i+1,j).text = str(df.values[i,j])
    except:
        doc = doc
        print('Unable to add table')

    doc.add_page_break()
    return doc

def save_word_document(doc, customer):
    doc.save('media/{}-AS_Built.docx'.format(customer))

def get_network_info(input_dict, append_url = '', dict_key ='', list=True):
    for network in input_dict:
        if append_url == 'l3FirewallRules':
            print('yee')
            print(meraki_data['networks'])
            print('yo')
            print(network)
        data, status_code = http_get(meraki_url='networks/{}/{}'.format(network["id"],
        append_url))
        print('url = {}  dict_key = {} status code = {}'.format(append_url, dict_key, status_code))
        print(input_dict[dict_key])
        if list == True:
            for i in data:
                if 'errors' not in i:
                    print(input_dict[dict_key])
                    input_dict[dict_key].append(i)
                else:
                    print("error found")
        elif list == False:
            input_dict[dict_key].append(data)


def pull_data(meraki_url='organizations'):
    # Intitialise dictionary to store returned data
    data, status_code = http_get(meraki_url)
    return data, status_code


def get_org_info(dn='networks'):
    data = []
    orgs, status_code = pull_data(meraki_url='organizations')
    try:
        data_df = pd.DataFrame.from_dict(orgs)
    except:
        data_df = pd.DataFrame.from_dict(orgs, orient='index')
    for org in orgs:
        # Get networks from all orgs and add to dictionary
        org_data, status_code = pull_data(
            meraki_url='organizations/{}/{}'.format(org["id"], dn))
        for i in org_data:
            data.append(i)
    return data, status_code, data_df


def get_network_info(network, append_url = ''):
    data, status_code = http_get(meraki_url='networks/{}/{}'.format(network["id"],
    append_url))
    print('url = {} status code = {}'.format(append_url, status_code))
    try:
        data_df = pd.DataFrame.from_dict(data)
    except:
        data_df = pd.DataFrame.from_dict(data, orient='index')
    pp.pprint(data_df)
    return data_df, status_code

'''
    meraki_data = {}
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
    meraki_data["contentFiltering"] = []
    meraki_data["intrusionSettings"] = []
    meraki_data["vlans"] = []
    meraki_data["traffic"] = []
    meraki_data["connectionStats"] = []
    meraki_data["clients"] = []
    meraki_data["staticRoutes"] = []
    meraki_data["uplinksLossAndLatency"] = []

    for customer in MerakiInfo.objects.all():
        print(customer.customer_name)
        customer = customer.customer_name

    for org in meraki_data['orgs']:
        # Get networks from all orgs and add to dictionary
        networks, status_code = http_get(
            meraki_url='organizations/{}/networks'.format(org["id"])
            )
        print(status_code)
        for network in networks:
            meraki_data["networks"].append(network)
            print(len(meraki_data['networks']))
            print(type(meraki_data['networks']))
            print(meraki_data['networks'])
        # Get license info from all orgs and add to dictionary
        licenses, status_code = http_get(
            meraki_url='organizations/{}/licenseState'.format(org["id"])
            )
        print(status_code)
        meraki_data["licenses"].append(licenses)

        # Get uplink info from all orgs and add to dictionary
        uplinksLossAndLatency, status_code = http_get(
            meraki_url='organizations/{}/uplinksLossAndLatency'.format(org["id"])
            )
        print(status_code)
        for uplink in uplinksLossAndLatency:
            meraki_data["uplinksLossAndLatency"].append(uplink)

        # Get IPs
        ips, status_code = http_get(
            meraki_url='organizations/{}/security/intrusionSettings'.format(
            org["id"]))
        print(status_code)
        for ip in ips:
            meraki_data["intrusionPrevention"].append(ip)


        def get_network_info(append_url = '', dict_key ='', list=True):
            if append_url == 'l3FirewallRules':
                print('yee')
                print(meraki_data['networks'])
                print('yo')
                print(network)
            data, status_code = http_get(meraki_url='networks/{}/{}'.format(network["id"],
            append_url))
            print('url = {}  dict_key = {} status code = {}'.format(append_url, dict_key, status_code))

            if list == True:
                for i in data:
                    if 'errors' not in i:
                        meraki_data[dict_key].append(i)
                    else:
                        print("error found")
            elif list == False:
                meraki_data[dict_key].append(data)




    get_network_info(meraki_data['networks'], append_url='devices', dict_key='devices')
    get_network_info(meraki_data['networks'], append_url='securityEvents', dict_key='securityEvents',
        list=False)
    get_network_info(meraki_data['networks'], append_url='ssids', dict_key='ssids')
    get_network_info(meraki_data['networks'], append_url='firewalledServices', dict_key='fwServices')
    get_network_info(meraki_data['networks'], append_url='l3FirewallRules', dict_key='l3FirewallRules',
        list=True)
    get_network_info(meraki_data['networks'], append_url='contentFiltering', dict_key='contentFiltering',
        list=False)
    get_network_info(meraki_data['networks'], append_url='security/intrusionSettings',
                    dict_key='intrusionSettings', list=False)

    get_network_info(meraki_data['networks'], append_url='vlans', dict_key='vlans')
    get_network_info(meraki_data['networks'], append_url='traffic?timespan=86400', dict_key='traffic')
    get_network_info(meraki_data['networks'], append_url='connectionStats?timespan=86400',
                    dict_key='connectionStats', list=False)
    get_network_info(meraki_data['networks'], append_url='clients', dict_key='clients')
    get_network_info(meraki_data['networks'], append_url='staticRoutes', dict_key='staticRoutes')


    licenses_df = pd.DataFrame.from_dict(meraki_data['licenses'])
    orgs_df = pd.DataFrame.from_dict(meraki_data['orgs'])
    networks_df = pd.DataFrame.from_dict(meraki_data['networks'])
    if len(meraki_data['vlans']) > 0:
        meraki_vlans_df = pd.DataFrame.from_dict(meraki_data['vlans'])
    staticRoutes_df = pd.DataFrame.from_dict(meraki_data['staticRoutes'])
    l3FirewallRules_df = pd.DataFrame.from_dict(meraki_data['l3FirewallRules'])
    contentFiltering_df = pd.DataFrame.from_dict(meraki_data['contentFiltering'])
    intrusionSettings_df = pd.DataFrame.from_dict(meraki_data['intrusionSettings'])
    ssids_df = pd.DataFrame.from_dict(meraki_data['ssids'])
    if len(meraki_data['devices']) > 0:
        devices_df = pd.DataFrame.from_dict(meraki_data['devices'])
    clients_df = pd.DataFrame.from_dict(meraki_data['clients'])
    traffic_df = pd.DataFrame.from_dict(meraki_data['traffic'])
    if len(meraki_data['connectionStats']) > 0:
        connectionStats_df = pd.DataFrame.from_dict(meraki_data['connectionStats'])
    uplinksLossAndLatency_df = pd.DataFrame.from_dict(meraki_data['uplinksLossAndLatency'])

    '''
'''
def word_report():

    doc = create_word_doc_title()

    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'License Overview',
        paragraph_text='\nThe following licenses were found:\n'
        )
    doc = create_word_doc_table(doc=doc,df=licenses_df)

    try:
        doc = create_word_doc_paragraph(
            doc = doc,
            heading_text = 'Device Overview',
            paragraph_text='The {} network includes the following devices:'.format(meraki_data['orgs'][0]['name'])
            )

        mr_qty, ms_qty, mx_qty, mv_qty = 0, 0, 0, 0
        for device in meraki_data['devices']:
            if 'MR' in device['model']:
                mr_qty += 1
            elif 'MS' in device['model']:
                ms_qty += 1
            elif 'MX' in device['model']:
                mx_qty += 1
            elif 'MV' in device['model']:
                mv_qty += 1
        doc = create_word_doc_bullet(
            doc = doc,
            bp1='{} MR Wireless Access Point(s)'.format(str(mr_qty)),
            bp2='{} MS Security appliances(s)'.format(str(ms_qty)),
            bp3='{} MX Security appliance(s)'.format(str(mx_qty)),
            bp4='() MV appliance(s)\n'.format(mv_qty)
            )
        doc = create_word_doc_table(doc=doc, df=devices_df)
    except:
        print('error adding devices')


    try:
        doc = create_word_doc_paragraph(
            doc = doc,
            heading_text = 'Layer 2',
            paragraph_text='\nThe following {} VLANs are configured:\n'.format(
                len(meraki_data['vlans']))
            )
        doc = create_word_doc_table(
            doc,
            meraki_vlans_df
            )
    except:
        print('Error adding vlans')


    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Uplinks',
        paragraph_text='\nDevice {} {} uplink\'s most recent loss percent is {}, latency {} ms:\n'.format(
            meraki_data["uplinksLossAndLatency"][0]['serial'],
            meraki_data["uplinksLossAndLatency"][0]['uplink'],
            meraki_data["uplinksLossAndLatency"][0]['timeSeries'][-1]['lossPercent'],
            meraki_data["uplinksLossAndLatency"][0]['timeSeries'][-1]['latencyMs'],
            )
        )
    doc = create_word_doc_table(
        doc,
        uplinksLossAndLatency_df
        )


    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Firewall Rules',
        paragraph_text='\nThe following {} rules are configured:\n'.format(
            len(meraki_data['l3FirewallRules']))
        )
    doc = create_word_doc_table(
        doc,
        l3FirewallRules_df
        )


    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Intrusion Settings',
        paragraph_text='\nThe following Intrusion Prevention Settings are configured:\n'
        )
    doc = create_word_doc_table(
        doc,
        intrusionSettings_df
        )


    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Content Filtering',
        paragraph_text='\nThe following Content Filtering Rules are configured:\n'
        )
    doc = create_word_doc_table(
        doc,
        contentFiltering_df
        )

    wired_qty, wireless_qty = 0, 0
    for client in meraki_data['clients']:
        if client['ssid'] != None:
            wireless_qty += 1
        elif client['ssid'] == None:
            wired_qty += 1
    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Client Overview',
        paragraph_text='\n{} wired and {} wireless clients have recently connected to the network:\n'.format(
        wired_qty, wireless_qty)
        )
    doc = create_word_doc_table(
        doc,
        clients_df
        )



    try:
        doc = create_word_doc_paragraph(
            doc = doc,
            heading_text = 'Connection Statistics',
            paragraph_text='\nBelow outlines client connections over the past 24 hours:\n'
            )
        doc = create_word_doc_table(
            doc,
            connectionStats_df
            )
    except:
        print('unable to add connection stats')

    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Traffic Overview',
        paragraph_text='\n{} outside destinations have been visited over the past 24 hours:\n'.format(
            len(meraki_data['traffic']))
        )
    doc = create_word_doc_table(
        doc,
        traffic_df
        )

    doc = create_word_doc_paragraph(
        doc = doc,
        heading_text = 'Wireless',
        paragraph_text='\nOf the {} SSIDs:\n'.format(
            len(meraki_data['ssids']))
        )

    enabled_qty, disabled_qty = 0, 0
    for ssid in meraki_data['ssids']:
        if ssid['enabled'] == True:
            enabled_qty += 1
        elif ssid['enabled'] == False:
            disabled_qty += 1
    doc = create_word_doc_bullet(
        doc = doc,
        bp1='{} is enabled'.format(str(enabled_qty)),
        bp2='{} is disabled\n'.format(str(disabled_qty)),
        )
    doc = create_word_doc_table(
        doc,
        ssids_df
        )


    doc.save('media/{}-AS_Built.docx'.format(customer))
'''
