from django.urls import path
from device import views
app_name = 'endnode'
urlpatterns = [
    path('', views.EndNode, name='endnode_page'),
    path('InfoEndNode/', views.InfoEndNode, name='endnode_info'),
    path('AddEndNode/', views.AddEndNode, name='add_endnode'),
    path('DeleteEndNode/', views.DeleteEndNode, name='delete_endnode'),
    path('TestConnect/', views.TestConnect, name='test_connect'),
]