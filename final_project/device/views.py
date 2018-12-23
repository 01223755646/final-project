from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from network.models import Network
import os
import sqlite3
from device.tests import GetInfoEndnode
# Create your views here.
@login_required(login_url='/account/UserLogin/')
def EndNode(request):
    print(request)
    return render(request,'device/endnode.html')

@login_required(login_url='/account/UserLogin/')
def InfoEndNode(request):
    print(request.POST)
    linkDB = "C:\\Users\\Admin\\Desktop\\final_project\\final_project\\db.sqlite3"
    data = GetInfoEndnode(linkDB)
    return JsonResponse(data)