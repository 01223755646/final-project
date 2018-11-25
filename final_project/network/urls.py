from django.urls import path
from network import views
app_name = 'network'
urlpatterns = [
    path('', views.Network, name='info_network'),
]