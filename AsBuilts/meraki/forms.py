from django import forms
from .models import MerakiInfo

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class MerakiInfoForm(forms.ModelForm):
    class Meta:
        model = MerakiInfo
        fields = (
                  'api_key',
                  'customer_name',
                 )
