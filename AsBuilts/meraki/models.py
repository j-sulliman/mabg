from django.db import models
from django.utils import timezone

# Create your models here.
class MerakiInfo(models.Model):
    api_key = models.CharField(max_length=200, primary_key=True,
    default='xxxxxxxxxxxx')
    customer_name = models.CharField(max_length=200, default="default")
    last_updated = models.DateTimeField(default=timezone.now)


class Licenses(models.Model):
    status = models.CharField(max_length=200)
    expirationDate = models.CharField(max_length=200, primary_key=True)
    licensedDeviceCounts = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expirationDate


class Vlans(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    networkId = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    applianceIp = models.CharField(max_length=200)
    subnet = models.CharField(max_length=200)
    fixedIpAssignments = models.CharField(max_length=200)
    reservedIpRanges = models.CharField(max_length=200)
    dnsNameservers = models.CharField(max_length=200)
    dhcpHandling = models.CharField(max_length=200)
    dhcpLeaseTime = models.CharField(max_length=200)
    dhcpBootOptionsEnabled = models.CharField(max_length=200)
    dhcpBootNextServer = models.CharField(max_length=200)
    dhcpBootFilename = models.CharField(max_length=200)
    dhcpOptions = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expirationDate


class l3FirewallRules(models.Model):
    comment = models.CharField(max_length=200)
    policy = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    srcport = models.CharField(max_length=200)
    srccidr = models.CharField(max_length=200)
    destport = models.CharField(max_length=200)
    destcidr = models.CharField(max_length=200)
    syslogEnabled = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expirationDate


class devices(models.Model):
    lat = models.CharField(max_length=200)
    lng = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    serial = models.CharField(max_length=200, primary_key=True)
    mac = models.CharField(max_length=200)
    wan1ip = models.CharField(max_length=200)
    wan2ip = models.CharField(max_length=200)
    lanip = models.CharField(max_length=200)
    networkId = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    switchProfileId = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expirationDate

class ssids(models.Model):
    lat = models.CharField(max_length=200)
    lng = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    serial = models.CharField(max_length=200, primary_key=True)
    mac = models.CharField(max_length=200)
    wan1ip = models.CharField(max_length=200)
    wan2ip = models.CharField(max_length=200)
    lanip = models.CharField(max_length=200)
    networkId = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    switchProfileId = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expirationDate

class clients(models.Model):
    id = models.CharField(max_length=200)
    mac = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    ip6 = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    firstseen = models.CharField(max_length=200)
    lastseen = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    recentDeviceSerial = models.CharField(max_length=200)
    recentDeviceName = models.CharField(max_length=200)
    recentDeviceMac = models.CharField(max_length=200)
    recentDeviceSerial = models.CharField(max_length=200)
    ssid = models.CharField(max_length=200)
    vlan = models.CharField(max_length=200)
    switchport = models.CharField(max_length=200)
    usage = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expirationDate
