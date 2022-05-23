from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth import authenticate , login ,logout
from .models import *
from .forms import  CreateUserForm ,LoginForm ,CreateAssociation , CreatePersonne

from django.contrib import messages
# Create your views here.


def Register (request):
    form = CreateUserForm()
    form2 = CreateAssociation()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            name = request.POST['name']
            file = request.POST['file']
            willaya = request.POST['willaya']
             
            user = form.save()
            Association.objects.create(
                    user=user ,
                    name=name ,
                    file=file,
                    willaya=willaya

            )

            messages.success(request,'account created seccefully ')
            return redirect('login')

    context= {'form':form ,'form2':form2} 
    return render(request,'signup.html',context)





def RegisterUser (request):
    form = CreateUserForm()
    form2 = CreatePersonne()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            name = request.POST['first_name']
            last_name = request.POST['last_name']
            willaya = request.POST['willaya']
             
            user = form.save()
            PhysicalUser.objects.create(
                    user=user ,
                    first_name=name ,
                    last_name=last_name,
                    willaya=willaya , 
            )

            messages.success(request,'account created seccefully ')
            return redirect('login')

    context= {'form':form ,'form2':form2} 
    return render(request,'physical.html',context)



def Loginin (request):
    form = LoginForm()
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user = authenticate(request , email=email,password=password )  
            if user is not None :
                login (request , user ) 
                return redirect('profile')
    context= {'form':form}
    return render(request,'login.html',context)

def Profile (request):
    
    context= {}
    return render(request,'profile.html',context)
def Select (request):
    
    context= {}
    return render(request,'select.html',context)


def Logoutt (request):
    logout(request)
    return redirect('login')

