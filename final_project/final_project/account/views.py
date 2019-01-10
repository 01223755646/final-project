from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) 
        # print(username, password, user)
        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'account/info.html') 
            else:
                render(request,'account/login.html',{'error':'ACCOUNT NOT ACTIVE!'})
        else:
            print("LOGIN FAILED!")
            print("Username: {} and password {}".format(username, password))
            return render(request,'account/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request,'account/login.html',{})

@login_required(login_url='/account/UserLogin/')
def ChangePassword(request):
    print(request.POST)
    if request.method == 'POST':
        if request.POST.get('new') == request.POST.get('confilm'):
            username = request.POST.get('name')
            password = request.POST.get('old')
            user = authenticate(username=username, password=password)
            if user:
                user.set_password(request.POST.get('new'))
                user.save()
                return JsonResponse({'status':'Successfull'})
            return JsonResponse({'status':'Old password is incorect'})
        return JsonResponse({'status':'Password does Not macth.'})
    return JsonResponse({'status':'Invalidate Data.'})

@login_required(login_url='/account/UserLogin/')
def Info(request):
    return render(request, 'account/info.html')

@login_required(login_url='/account/UserLogin/')
def UserLogout(request):
    logout(request)
    return render(request, 'account/login.html')