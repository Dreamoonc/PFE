from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth import authenticate , login ,logout
from .models import *
from .forms import  *
from django.contrib import messages


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
            user.is_association =True
            user.save()
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
            user.is_person =True
            user.save()
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

def annonce (request):
    annonces= Annonce.objects.all()
    formAnnonce = AnnonceForm()
    if request.method =='POST':
        auteur= request.user
        if formAnnonce.is_valid :
            image = request.FILES['image']
            contenu = request.POST['contenu']
            type = request.POST['type']
            Annonce.objects.create(
                auteur = auteur,
                image = image ,
                contenu =contenu ,
                type = type 
            )
            return redirect('annonce')

    context= {'formAnnonce':formAnnonce , 'annonces':annonces}
    return render(request,'annonce.html',context)

def delete_annonce (request,myid) :
    item = Annonce.objects.get(id =myid)
    item.delete()
    messages.info(request,'Annonce supprimé')
    return redirect(annonce)

def ListCagniote (request):
    cagnites= Cagniote.objects.all()
    form = CreateCagniote ()
    if request.method =='POST':
        username = request.user
        association = Association.objects.get(user=username)
        if form.is_valid :
            titre = request.POST['titre']
            contenu = request.POST['contenu']
            somme = request.POST['sommeDemander']
            Cagniote.objects.create(
                user = association,
                titre = titre ,
                contenu =contenu ,
                sommeDemander = somme 
            )

    context= {'form':form , 'cagniotes':cagnites}
    return render(request,'cagniote.html',context)


def Admin (request):
    
    context= {}
    return render(request,'admin.html',context)
