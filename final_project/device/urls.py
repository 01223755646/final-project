from django.urls import path
from device import views
app_name = 'endnode'
urlpatterns = [
    path('', views.EndNode, name='info_endnode'),
]