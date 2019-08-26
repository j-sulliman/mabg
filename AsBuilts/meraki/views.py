from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import reverse
from .models import MerakiInfo
from .forms import MerakiInfoForm
from .tables import MerakiInfoForm_table
from .applications.meraki import pull_data
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
                print(i.api_key)
                customer = i.customer_name
                pull_data()
                return redirect('/media/{}-AS_Built.docx'.format(customer))

    else:
        form = MerakiInfoForm()
    return render(request, 'meraki/defaults.html', {
        'form': form})
    #HttpResponseRedirect('media/{}-AS_Built.docx'.format)
