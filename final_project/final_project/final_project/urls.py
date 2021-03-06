"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# views of webapp 
from account import views as account_views
from device import views as device_views
from network import views as network_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.Info, name='Info'),
    path('account/', include('account.urls', namespace='account')),
    path('Logout/', account_views.UserLogout, name='Logout'),
    path('network/', include('network.urls')),
    path('device/', include('device.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
