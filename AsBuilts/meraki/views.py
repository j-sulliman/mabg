from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import reverse
from .models import MerakiInfo
from .forms import MerakiInfoForm
from .tables import MerakiInfoForm_table
from .applications.meraki import pull_data, get_org_info, get_network_info
from .applications.meraki import create_word_doc_title, create_word_doc_paragraph
from .applications.meraki import create_word_doc_table, create_word_doc_bullet
from .applications.meraki import save_word_document, create_word_doc_text
from .applications.meraki import ins_word_doc_image
import os, re, os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return HttpResponse("Meraki As Built Generator.")


#@login_required
def defaults_form(request):
    log_data = []
    saved = False
    customer = ''
    if request.method == "POST":
        form = MerakiInfoForm(request.POST)
        MerakiInfo.objects.all().delete()
        #ObjectConfigurationStatus.objects.all().delete()
        if form.is_valid():
            for root, dirs, files in os.walk('media/tmp'):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.mkdir('media/tmp')
            post = form.save(commit=False)
            #post.name = request.user
            #post.published_date = timezone.now()
            post.save()
            doc = create_word_doc_title()
            for i in MerakiInfo.objects.all():
                customer = i.customer_name

                # Get Organisational Level Data
                networks, status_code, orgs_df, networks_df = get_org_info(dn='networks')
                log_data.append(status_code)
                licenseState, status_code, orgs_df, licenseState_df = get_org_info(dn='licenseState')
                log_data.append(status_code)
                uplinksLossAndLatency, status_code, orgs_df, uplinksLossAndLatency_df = get_org_info(dn='uplinksLossAndLatency')
                log_data.append(status_code)



                # Licenses Section of Document
                doc = create_word_doc_paragraph(doc = doc,
                    heading_text = 'License Overview',
                    paragraph_text='\n{} has the following licenses:\n'.format(customer))
                doc = create_word_doc_table(doc=doc,df=licenseState_df)

                # Networks Section of Document
                doc = create_word_doc_paragraph(doc = doc,
                    heading_text = 'Networks Overview',
                    paragraph_text='\nThe following Networks were found:\n')
                doc = create_word_doc_table(doc=doc,df=networks_df)

                # Uplinks Section of Document
                doc = create_word_doc_paragraph(doc = doc,
                    heading_text = 'Uplinks',
                    paragraph_text='\nThe following Uplinks were found:\n')
                doc = create_word_doc_table(doc=doc,df=uplinksLossAndLatency_df)

                # Get Network Level Data
                for network in networks:
                    devices, status_code = get_network_info(network,
                    append_url='devices')

                    if isinstance(devices, pd.DataFrame) and 'firmware' in devices.columns:
                        unique_fw = devices['firmware'].value_counts()
                        unique_fw.plot.pie()
                        plt.savefig('media/tmp/firmware.png', bbox_inches="tight")
                        plt.clf()

                        unique_models = devices['model'].value_counts()
                        unique_models.plot.bar(x = 'model', y = 'count', rot = 0)
                        plt.savefig('media/tmp/models.png', bbox_inches="tight")
                        plt.clf()

                    log_data.append(status_code)
                    securityEvents, status_code = get_network_info(network,
                    append_url='securityEvents')
                    log_data.append(status_code)
                    ssids, status_code = get_network_info(network,
                    append_url='ssids')
                    log_data.append(status_code)
                    firewalledServices, status_code = get_network_info(network,
                    append_url='firewalledServices')
                    log_data.append(status_code)
                    l3FirewallRules, status_code = get_network_info(network,
                    append_url='l3FirewallRules')
                    log_data.append(status_code)
                    contentFiltering, status_code = get_network_info(network,
                    append_url='contentFiltering')
                    log_data.append(status_code)
                    intrusionSettings, status_code = get_network_info(network,
                    append_url='security/intrusionSettings')
                    log_data.append(status_code)
                    malwareSettings, status_code = get_network_info(network,
                    append_url='security/malwareSettings')
                    log_data.append(status_code)
                    vlans, status_code = get_network_info(network,
                    append_url='vlans')
                    log_data.append(status_code)
                    traffic, status_code = get_network_info(network,
                    append_url='traffic?timespan=86400')
                    log_data.append(status_code)
                    if isinstance(traffic, pd.DataFrame) and 'sent' in traffic.columns:
                        traffic_top_sent = traffic.nlargest(10, 'sent')
                        traffic_top_sent.plot(x = 'application', y= 'sent', kind = 'barh')
                        plt.savefig('media/tmp/top_traffic_sent.png', bbox_inches="tight")
                        plt.clf()

                        traffic_top_recv = traffic.nlargest(10, 'recv')
                        traffic_top_recv.plot(x = 'application', y= 'recv', kind = 'barh')
                        plt.savefig('media/tmp/top_traffic_recv.png', bbox_inches="tight")
                        plt.clf()

                    connectionStats, status_code = get_network_info(network,
                    append_url='connectionStats?timespan=86400')
                    log_data.append(status_code)
                    clients, status_code = get_network_info(network,
                    append_url='clients')
                    log_data.append(status_code)


                    if isinstance(clients, pd.DataFrame) and 'os' in clients.columns:
                        print('clients it is')
                        unique_mfr = clients['manufacturer'].value_counts()
                        unique_mfr.plot.barh(x = 'client', y = 'count', rot = 0)
                        plt.savefig('media/tmp/clients.png', bbox_inches="tight")
                        plt.clf()

                    staticRoutes, status_code = get_network_info(network,
                    append_url='staticRoutes')
                    log_data.append(status_code)


                    # Devices Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Devices Overview',
                        paragraph_text='\n{} has the following Devices in network {}:\n'.format(customer, network['name'])
                        )
                    if os.path.isfile('media/tmp/models.png'):
                        doc = ins_word_doc_image(doc = doc, pic_dir='media/tmp/models.png',
                            pic_width=5.25)
                        os.remove("media/tmp/models.png")
                    if os.path.isfile('media/tmp/firmware.png'):
                        doc = ins_word_doc_image(doc = doc, pic_dir='media/tmp/firmware.png',
                            pic_width=5.25)
                        os.remove("media/tmp/firmware.png")

                    doc = create_word_doc_table(doc=doc,df=devices)

                    # VLANs Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'VLANs',
                        paragraph_text='\n{} has the following VLANs configured for network {}:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=vlans)

                    # Static Routes Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Static Routes',
                        paragraph_text='\n{} has the following Static Routes configured for network {}:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=staticRoutes)

                    # Wireless Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Wireless Networks',
                        paragraph_text='\n{} has the following SSIDs configured in network {}:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=ssids)

                    # Wireless Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Clients',
                        paragraph_text='\n{} has the following Wireless Clients in network {}:\n'.format(customer, network['name']))
                    if os.path.isfile('media/tmp/clients.png'):
                        doc = ins_word_doc_image(doc = doc, pic_dir='media/tmp/clients.png',
                            pic_width=5.25)
                        os.remove("media/tmp/clients.png")
                    doc = create_word_doc_table(doc=doc,df=clients)

                    # Services Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Firewall Services',
                        paragraph_text='\nThe following services are configured in {}\'s network {}:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=firewalledServices)

                    # L3 Firewall Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'L3 Firewall Rules',
                        paragraph_text='\nThe following L3 Firewall rules are configured in {}\'s network {}:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=l3FirewallRules)

                    # L3 Firewall Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Content Filtering',
                        paragraph_text='\nThe following Content Filtering Rules are configured:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=contentFiltering)

                    # IPS Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Intrusion Prevention',
                        paragraph_text='\nThe following Intrusion Prevention Settings are configured:\n')
                    doc = create_word_doc_table(doc=doc,df=intrusionSettings)

                    # Malware Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Intrusion Prevention',
                        paragraph_text='\nThe following Malware  Settings are configured:\n')
                    doc = create_word_doc_table(doc=doc,df=malwareSettings)

                    # Traffic Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Network Traffic',
                        paragraph_text='\nThe following shows the top two senders detected for {}, network {} over the past 24 hours:\n'.format(customer, network['name']))
                    if os.path.isfile('media/tmp/top_traffic_sent.png'):
                        doc = ins_word_doc_image(doc = doc, pic_dir='media/tmp/top_traffic_sent.png',
                            pic_width=5.25)
                        os.remove("media/tmp/top_traffic_sent.png")
                    if os.path.isfile('media/tmp/top_traffic_recv.png'):
                        doc = ins_word_doc_image(doc = doc, pic_dir='media/tmp/top_traffic_recv.png',
                            pic_width=5.25)
                        os.remove("media/tmp/top_traffic_recv.png")
                    #traffic_top_sent = traffic.nlargest(50, 'sent')
                    doc = create_word_doc_table(doc=doc,df=traffic)

                    # Connection Stats
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Connection Statistics',
                        paragraph_text='\nConnection Statistics for {}\'s network {}:\n'.format(customer, network['name']))
                    doc = create_word_doc_table(doc=doc,df=connectionStats)

                # Logfile Section of Document
                doc = create_word_doc_paragraph(doc = doc,
                    heading_text = '**Logfile for reference - delete**',
                    paragraph_text='\nThe status code for API requests are outlined below for reference:\n')
                for log in log_data:
                    create_word_doc_text(log, doc = doc)

                save_word_document(doc = doc, customer = customer)




        return redirect('/media/tmp/{}-AS_Built.docx'.format(customer))

    else:
        form = MerakiInfoForm()
    return render(request, 'meraki/defaults.html', {
        'form': form})
