from django.contrib import admin
from network.models import Network
# Register your models here.
@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ['ID', 'MODE', 'SSID', 'PSK', 'IP', 'GateWay', 'SubnetMask', 'IP_Mode', 'SignalStrength', 'Update']