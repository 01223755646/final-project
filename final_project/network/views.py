from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from network.models import Network
import os
import sqlite3
# Create your views here.
@login_required(login_url='/account/UserLogin/')
def Network_(request):
    print(request)
    return render(request,'network/network.html')

@login_required(login_url='/account/UserLogin/')
def Accesspoint(request):
    print(request.POST)
    network_ = Network.objects.get()
    network_.SSID = request.POST['SSID']
    network_.PSK = request.POST['PSK']
    network_.MODE = request.POST['Mode']
    network_.save()
    return render(request,'network/network.html')

@login_required(login_url='/account/UserLogin/')
def StaticWifiStation(request):
    print(request.POST)
    network_ = Network.objects.get()
    network_.SSID = request.POST['SSID']
    network_.PSK = request.POST['PSK']
    network_.MODE = request.POST['Mode']
    network_.IP = request.POST['IP']
    network_.SubnetMask = request.POST['SUBNET']
    network_.GateWay = request.POST['GATEWAY']
    network_.save()
    return render(request,'network/network.html')

@login_required(login_url='/account/UserLogin/')
def HDCPWifiStation(request):
    print(request.POST)
    network_ = Network.objects.get()
    network_.SSID = request.POST['SSID']
    network_.PSK = request.POST['PSK']
    network_.MODE = request.POST['Mode']
    network_.save()
    return render(request,'network/network.html')
