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
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
            for i in MerakiInfo.objects.all():
                print('API Key is {}'.format(i.api_key))
                print('Customer is {}'.format(i.customer_name))
                customer = i.customer_name
                networks, status_code = get_org_info(dn='networks')
                licenses, status_code = get_org_info(dn='licenseState')
                uplinks, status_code = get_org_info(dn='uplinksLossAndLatency')
                ips, status_code = get_org_info(dn='security/intrusionSettings')
                malware, status_code = get_org_info(dn='security/malwareSettings')
                l3fw, status_code = get_org_info(dn='security/l3FirewallRules')
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
                    devices, status_code = get_network_info(network,
                    append_url='vlans')
                    traffic, status_code = get_network_info(network,
                    append_url='traffic?timespan=86400')
                    connectionStats, status_code = get_network_info(network,
                    append_url='connectionStats?timespan=86400')
                    clients, status_code = get_network_info(network,
                    append_url='clients')
                    staticRoutes, status_code = get_network_info(network,
                    append_url='staticRoutes')
                    print(devices)

                return redirect('/media/{}-AS_Built.docx'.format(customer))

    else:
        form = MerakiInfoForm()
    return render(request, 'meraki/defaults.html', {
        'form': form})
    #HttpResponseRedirect('media/{}-AS_Built.docx'.format)
