import django_tables2 as tables
from .models import MerakiInfo

class MerakiInfoForm_table(tables.Table):
    class Meta:
        model = MerakiInfo
        template_name = 'django_tables2/semantic.html'
