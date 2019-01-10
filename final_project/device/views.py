from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from network.models import Network
import os
import sqlite3
from device.tests import GetInfoEndnode, CheckIDNode, CheckExist, AddEndNode_, DeleteEndNode_, getdataCMpage, ControlRELAY
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
@login_required(login_url='/account/UserLogin/')

def AddEndNode(request):
    print(request.POST)
    data = {}
    linkDB = "C:\\Users\\Admin\\Desktop\\final_project\\final_project\\db.sqlite3"
    if request.method == 'POST':
        TYPENODE = request.POST['TYPENODE']
        IDNODE = request.POST['IDNODE']
        if CheckIDNode(TYPENODE, IDNODE):
            if CheckExist(linkDB, IDNODE) == False:
                AddEndNode_(linkDB, TYPENODE, IDNODE)
            else:
                JsonResponse({'status':'error'})
        else:
            JsonResponse({'status':'error'})

    return JsonResponse(data)

@login_required(login_url='/account/UserLogin/')
def DeleteEndNode(request):
    print(request.POST)
    data = {}
    linkDB = "C:\\Users\\Admin\\Desktop\\final_project\\final_project\\db.sqlite3"
    if request.method == 'POST':
        TYPENODE = request.POST['TYPENODE']
        IDNODE = request.POST['IDNODE']
        if CheckIDNode(TYPENODE, IDNODE):
            if CheckExist(linkDB, IDNODE) == True:
                DeleteEndNode_(linkDB, TYPENODE, IDNODE)
            else:
                JsonResponse({'status':'error'})
        else:
            JsonResponse({'status':'error'})
    return JsonResponse(data)

@login_required(login_url='/account/UserLogin/')
def TestConnect(request):
    print(request.POST)
    if request.method == 'POST':
        IDNODE = request.POST['IDNODE']
        TYPENODE = IDNODE[:(len(IDNODE)-2)]
        if CheckIDNode(TYPENODE, IDNODE):
            print('OK! Send request')
    data = {}
    return JsonResponse(data)

@login_required(login_url='/account/UserLogin/')
def ControlMornitoringPage(request):
    print(request)
    return render(request,'ControlMornitoring/CMPages.html')

@login_required(login_url='/account/UserLogin/')
def DataCMPage(request):
    linkDB = "C:\\Users\\Admin\\Desktop\\final_project\\final_project\\db.sqlite3"
    if request.method == 'POST':
        data = getdataCMpage(linkDB)
        return JsonResponse(data)
    return render(request,'ControlMornitoring/CMPages.html')

@login_required(login_url='/account/UserLogin/')
def ControlDO(request):
    # print((request.POST))
    linkDB = "C:\\Users\\Admin\\Desktop\\final_project\\final_project\\db.sqlite3"
    if request.method == 'POST':
        IDNODE  = request.POST['IDNODE']
        
        STATUS  = request.POST['STATUS']
        NODE    = IDNODE[:(len(IDNODE)-2)]

        if NODE == 'RLACS':
            PIN     = request.POST['PIN'] + 'X'
            order_query = ''' UPDATE {} SET {} = "{}" WHERE IDNODE = "{}"  '''.format(NODE, PIN, STATUS, IDNODE)
        elif NODE == 'RLTDS' :
            PIN     = request.POST['PIN']
            order_query = ''' UPDATE {} SET {} = "{}" WHERE IDNODE = "{}"  '''.format(NODE, PIN, STATUS, IDNODE)
        # print(order_query)
        ControlRELAY(linkDB, order_query)
    return JsonResponse({})