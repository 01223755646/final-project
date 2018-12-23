from django.urls import path
from network import views
app_name = 'network'
urlpatterns = [
    path('', views.Network_, name='info_network'),
    path('Accesspoint/', views.Accesspoint, name='config_accesspoint'),
    path('StaticWS/', views.StaticWifiStation, name='config_StaticWS'),
    path('DHCPWS/', views.HDCPWifiStation, name='config_DHCPWS'),
]