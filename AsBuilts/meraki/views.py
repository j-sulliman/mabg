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
from .applications.meraki import save_word_document
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return HttpResponse("Meraki As Built Generator.")

def download(request, path):

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
'''
def download_docx(request):
    for i in MerakiInfo.objects.all():
        customer = i.customer_name
    with open('meraki/applications/{}-AS_Built.docx'.format(customer), 'rb') as doc:
    	response = HttpResponse(doc.read())
    	reponse['content_type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    	response['Content-Disposition'] = 'attachment;filename=file.docx'
    	return response
'''

@login_required
def defaults_form(request):
    saved = False
    customer = ''
    if request.method == "POST":
        form = MerakiInfoForm(request.POST)
        MerakiInfo.objects.all().delete()
        #ObjectConfigurationStatus.objects.all().delete()
        if form.is_valid():
            post = form.save(commit=False)
            #post.name = request.user
            #post.published_date = timezone.now()
            post.save()
            doc = create_word_doc_title()
            for i in MerakiInfo.objects.all():
                print('API Key is {}'.format(i.api_key))
                print('Customer is {}'.format(i.customer_name))
                customer = i.customer_name

                # Get Organisational Level Data
                networks, status_code, networks_df = get_org_info(dn='networks')
                licenses, status_code, licenseState_df = get_org_info(dn='licenseState')
                uplinks, status_code, uplinksLossAndLatency_df = get_org_info(dn='uplinksLossAndLatency')
                ips, status_code, intrusionSettings_df = get_org_info(dn='security/intrusionSettings')
                malware, status_code, malwareSettings_df = get_org_info(dn='security/malwareSettings')
                l3fw, status_code, l3FirewallRules_df = get_org_info(dn='security/l3FirewallRules')

                # Licenses Section of Document
                doc = create_word_doc_paragraph(doc = doc,
                    heading_text = 'License Overview',
                    paragraph_text='\nThe following licenses were found:\n')
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
                    securityEvents, status_code = get_network_info(network,
                    append_url='securityEvents')
                    ssids, status_code = get_network_info(network,
                    append_url='ssids')
                    firewalledServices, status_code = get_network_info(network,
                    append_url='firewalledServices')
                    l3FirewallRules, status_code = get_network_info(network,
                    append_url='l3FirewallRules')
                    contentFiltering, status_code = get_network_info(network,
                    append_url='contentFiltering')
                    intrusionSettings, status_code = get_network_info(network,
                    append_url='security/intrusionSettings')
                    vlans, status_code = get_network_info(network,
                    append_url='vlans')
                    traffic, status_code = get_network_info(network,
                    append_url='traffic?timespan=86400')
                    connectionStats, status_code = get_network_info(network,
                    append_url='connectionStats?timespan=86400')
                    clients, status_code = get_network_info(network,
                    append_url='clients')
                    staticRoutes, status_code = get_network_info(network,
                    append_url='staticRoutes')


                    # Devices Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Devices Overview',
                        paragraph_text='\nThe following Devices were found:\n')
                    doc = create_word_doc_table(doc=doc,df=devices)

                    # VLANs Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'VLANs',
                        paragraph_text='\nThe following Devices were found:\n')
                    doc = create_word_doc_table(doc=doc,df=vlans)

                    # Static Routes Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Static Routes',
                        paragraph_text='\nThe following Static Routes were found:\n')
                    doc = create_word_doc_table(doc=doc,df=staticRoutes)

                    # Wireless Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Devices Overview',
                        paragraph_text='\nThe following Uplinks were found:\n')
                    doc = create_word_doc_table(doc=doc,df=ssids)

                    # Wireless Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Clients',
                        paragraph_text='\nThe following Wireless Clients were found:\n')
                    doc = create_word_doc_table(doc=doc,df=clients)

                    # Services Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Firewall Services',
                        paragraph_text='\nThe following Rules are configured:\n')
                    doc = create_word_doc_table(doc=doc,df=firewalledServices)

                    # L3 Firewall Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'L2 Firewall Rules',
                        paragraph_text='\nThe following Rules are configured:\n')
                    doc = create_word_doc_table(doc=doc,df=l3FirewallRules)

                    # L3 Firewall Clients Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Content Filtering',
                        paragraph_text='\nThe following Content Filtering Rules are configured:\n')
                    doc = create_word_doc_table(doc=doc,df=contentFiltering)

                    # IPS Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Intrusion Prevention',
                        paragraph_text='\nThe following Intrusion Prevention Settings are configured:\n')
                    doc = create_word_doc_table(doc=doc,df=intrusionSettings)

                    # Traffic Section of Document
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Network Traffic',
                        paragraph_text='\nThe following Network Traffic has been detected:\n')
                    doc = create_word_doc_table(doc=doc,df=traffic)

                    # Connection Stats
                    doc = create_word_doc_paragraph(doc = doc,
                        heading_text = 'Network Traffic',
                        paragraph_text='\nThe following Network Traffic has been detected:\n')
                    doc = create_word_doc_table(doc=doc,df=connectionStats)

                save_word_document(doc = doc, customer = customer)




        return redirect('/media/{}-AS_Built.docx'.format(customer))

    else:
        form = MerakiInfoForm()
    return render(request, 'meraki/defaults.html', {
        'form': form})
    #HttpResponseRedirect('media/{}-AS_Built.docx'.format)
