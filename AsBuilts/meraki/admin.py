from django.contrib import admin
from .models import Licenses, Vlans, l3FirewallRules, devices, ssids, clients

# Register your models here.
admin.site.register(Licenses)
admin.site.register(Vlans)
admin.site.register(l3FirewallRules)
admin.site.register(devices)
admin.site.register(ssids)
admin.site.register(clients)
