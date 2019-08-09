from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import reverse
from .models import MerakiInfo
from .forms import MerakiInfoForm
from .tables import MerakiInfoForm_table
from .applications.meraki import pull_data

from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required
def defaults_form(request):
    saved = False
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
                pull_data()
    else:
        form = MerakiInfoForm()
    return render(request, 'meraki/defaults.html', {
        'form': form})
