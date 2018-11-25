from django.urls import path
from account import views
app_name = 'account'
urlpatterns = [
    path('UserLogin/', views.UserLogin, name='user_login'),
    path('ChangePass/', views.ChangePassword, name='change_pass'),
    path('Info/', views.Info, name='info'),
]