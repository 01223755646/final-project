from django.db import models

# Create your models here.
class Network(models.Model):
    ID              = models.AutoField(primary_key = True)
    MODE            = models.CharField(max_length = 20, default = "Wifi Station")
    SSID            = models.CharField(max_length = 50, default = "Thanh Thao_plus")
    PSK             = models.CharField(max_length = 50, default = "chaobuoisang")
    IP              = models.CharField(max_length = 20, default = "192.168.2.1")
    GateWay         = models.CharField(max_length = 20, default = "192.168.2.1")
    SubnetMask      = models.CharField(max_length = 20, default = "255.255.255.0")
    IP_Mode         = models.CharField(max_length = 20, default = "DHCP")
    SignalStrength  = models.CharField(max_length = 10, default = 'Good')
    Update          = models.DateTimeField(auto_now = True, blank = True)