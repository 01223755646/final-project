from django.urls import path
from device import views
app_name = 'endnode'
urlpatterns = [
    path('', views.EndNode, name='endnode_page'),
    path('InfoEndNode/', views.InfoEndNode, name='endnode_info'),
]