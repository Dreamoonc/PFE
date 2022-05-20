from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login , logout
from .models import *
from .forms import  CreateUserForm

from django.contrib import messages
# Create your views here.

def Profile (request):
    
    return render(request,'profile.html')


def Register (request):
    form = CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'account created seccefully ')
            return redirect('login')

    context= {'form':form}
    return render(request,'signup.html',context)


def Login (request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = authenticate(request, username=username , passeword=password)
        if user is not None :
            login(request, user)
            return redirect('profile')
        else :
            messages.info(request,'username or passeword false')

    context= {}
    return render(request,'login.html',context)