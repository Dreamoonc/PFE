from audioop import reverse
from xml.dom.pulldom import parseString
from django.shortcuts import  get_object_or_404, redirect, render
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate , login ,logout
from .models import *
from django.core.paginator import Paginator 
from .forms import  *
from django.contrib import messages
from .filters import *
from django.contrib.auth.forms import UserChangeForm ,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView ,View
from django.views import generic
from django.contrib import messages
from .consumers import TestConsumer

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes  , DjangoUnicodeDecodeError
from .utils import token_generator
from django.contrib.auth.decorators import login_required

import smtplib
creds={
    "email":"mdjassia@outlook.fr",
    "pass":"assiaqueen2001"
}

def SendGmail(People,title, Subject, msg):
    try:
        server = smtplib.SMTP("smtp.office365.com:587")
        server.ehlo()
        server.starttls()
        server.login(creds["email"], creds["pass"])
        message = "Subject: {}\n\n{}".format(Subject, msg)
        server.sendmail(f"{title} <{creds['email']}>", People, message)
        print("email has been sent")
    except Exception as e:
        print(("error",e))
        
def Register (request):
    form = CreateUserForm()
    form2 = CreateAssociation()
    form3 =CreateLocalisation()
    local = localisation.objects.all()
    wilaya = localisation.objects.values("wilaya_name").distinct()
    print(wilaya)
    if request.method =='POST':
        form = CreateUserForm(request.POST)   
        if form.is_valid():
            if  request.FILES:
                file = request.FILES['file']
            adress = request.POST['email']
            type = request.POST['type']
            category = request.POST['category']
            commune = request.POST['commune_name']
            daira = request.POST['daira_name']
            wilaya = request.POST['wilaya_name']
            
            loc_id = localisation.objects.filter(commune_name__icontains=commune , daira_name__icontains=daira , wilaya_name__icontains=wilaya  )
            print(loc_id)
         
            user = form.save()
            user.is_active= False 
            user.is_association =True
            
            user.save()
            Association.objects.create(
                    user=user ,
                    file=file,
                    type = type ,
                    category = category,
                    adresse = loc_id[0]
            )
            
            uidb64 = urlsafe_base64_encode (force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('ActiverCompte',kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
            link1 = reverse('validerCompte',kwargs={'pk':user.email})
            url = 'http://'+domain+link
            emailbody = "hi"+ user.username+'please use this link to verify ur account \n'+url
            url1 = 'http://'+domain+link1
            body = "hi"+ user.username+'please use this link to verify ur account \n'+url1

            SendGmail([user.email], "title","email confirmation ",body)

            messages.success(request,' Confirmer votre compte  ')
            return redirect('login')

    context= {'form':form ,'form2':form2 , "form3":form3,"local":local, 'wilaya':wilaya } 
    return render(request,'signup.html',context)

def RegisterUser (request):
    form = CreateUserForm()
    form2 = CreatePersonne()
    form3 = CreateLocalisation()
    wilaya = localisation.objects.values("wilaya_name").distinct()
    local = localisation.objects.all()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            name = request.POST['first_name']
            last_name = request.POST['last_name']        
            commune = request.POST['commune_name']
            daira = request.POST['daira_name']
            wilaya = request.POST['wilaya_name']            
            loc_id = localisation.objects.filter(commune_name__icontains=commune , daira_name__icontains=daira , wilaya_name__icontains=wilaya  )
            
             
            user = form.save()
            user.is_person =True
            user.save()
            PhysicalUser.objects.create(
                    user=user ,
                    first_name=name ,
                    last_name=last_name,
                    adresse = loc_id[0]
            )
            uidb64 = urlsafe_base64_encode (force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('ActiverCompte',kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
            link1 = reverse('validerCompte',kwargs={'pk':user.email})
            url = 'http://'+domain+link
            emailbody = "hi"+ user.username+'please use this link to verify ur account \n'+url
            url1 = 'http://'+domain+link1
            body = "hi"+ user.username+'please use this link to verify ur account \n'+url1

            SendGmail([user.email], "title","email confirmation ",body)

            messages.success(request,'confirmer votre email')
            return redirect('login')

    context= {'form':form ,'form2':form2 , "form3" :form3,"local":local,'wilaya':wilaya} 
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
                if user.is_admin ==True :
                    return redirect('control') 
                if user.is_active == True : 
                    if  user.is_association :
                        ass = Association.objects.get(user = user)
                        if ass.is_valid == True :
                            login (request , user ) 
                            return redirect('profile')
                        else :
                            messages.error(request , "cette association n'est pas valide")
                else :
                    messages.error(request , "ce compte  n'est pas valide")
            else :
                login (request , user ) 
                return redirect('profile')           
    context= {'form':form}
    return render(request,'login.html',context)

class UserEdit (generic.UpdateView):
    form_class=EditProfileForm
    template_name= 'profile.html'
    success_url=reverse_lazy('profile')
    def get_object(self):
        return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annonces'] = Annonce.objects.filter(auteur=self.request.user)
        if self.request.user.is_person == True:
            context['info']=PhysicalUser.objects.get(user=self.request.user)
        elif self.request.user.is_association == True:
            context['info']=Association.objects.get(user=self.request.user)
        return context

class ShowProfilePersonne(DetailView):
    model=User
    template_name= 'personneProfile.html'
    def get_context_data(self, *args,**kwargs):
        profile=User.objects.all()
        context=super(ShowProfilePersonne,self).get_context_data(*args,**kwargs)
        page_user = get_object_or_404(User,id=self.kwargs['pk'])
        context['page_user']=page_user
        auteur=User.objects.get(id=self.kwargs['pk'])
        context['annonces']=Annonce.objects.filter(auteur=auteur)
        if auteur.is_person == True:
            context['info']=PhysicalUser.objects.get(user=auteur)
        elif auteur.is_association == True:
            context['info']=Association.objects.get(user=auteur)
        return context

class PasswordChange (PasswordChangeView):
    form_class=PasswordForm
    template_name='passwordChange.html'
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request,'password_success.html')

def updateAnnonce (request,pk):
    itemup = Annonce.objects.get(id =pk)
    formAnnonce=AnnonceForm(instance = itemup)
    if request.method == 'POST' :
        formAnnonce=AnnonceForm(request.POST, request.FILES, instance=itemup)
        if formAnnonce.is_valid():
            formAnnonce.save()
            return redirect('annonce')
    context={'formAnnonce':formAnnonce}    
    return render(request,'annonce.html',context)
   
def Select (request):
    
    context= {}
    return render(request,'select.html',context)

def Logoutt (request):
    logout(request)
    return redirect('login')

@login_required(login_url='../login/')
def annonce (request):
    annonces= Annonce.objects.all()
    notifications=Notification.objects.all()
    
    a= AnnonceFilter(request.GET, queryset=annonces)
    annonces=a.qs
    formAnnonce=AnnonceForm()
    if request.method =='POST':
        auteur= request.user
        if formAnnonce.is_valid :
            if request.FILES:
                image = request.FILES['image']
            else:
                image = request.POST['image']
            contenu = request.POST['contenu']
            type = request.POST['type']
            category= request.POST['category']
            Annonce.objects.create(
                auteur = auteur,
                image = image ,
                contenu =contenu ,
                type = type ,
                category=category
            )
            return redirect('annonce')
        else:
            formAnnonce = AnnonceForm()
    commentForm=CommentForm()
    context= {'formAnnonce':formAnnonce , 'annonces':annonces ,'commentForm':commentForm,'filter':a,'notifications':notifications}
    return render(request,'annonce.html',context)

def add_comment (request,myid,notifid):
    formComment=CommentForm()
    if request.method == "POST":
        auteur=request.user
        annonce=Annonce.objects.get(id=myid)
        user_notif=User.objects.get(id=notifid)
        if formComment.is_valid:
            contenu=request.POST['contenu']
            Comment.objects.create(
                auteur=auteur,
                contenu=contenu,
                annonce=annonce
            )
            Notification.objects.create(
                user=user_notif,
                notification="Vous avez un nouveau commentaire"    
            )
            return redirect('annonce')
        else:
            formComment=CommentForm()
    context={}
    return render(request,'annonce.html',context)

def delete_annonce (request,myid) :
    item = Annonce.objects.get(id =myid)
    item.delete()
    messages.info(request,'Annonce supprimé')
    return redirect(annonce)

def delete_comment (request,myid):
    item=Comment.objects.get(id=myid)
    item.delete()
    messages.info(request,'commentaire supprimé')
    return  redirect(annonce)

def signaler_annonce (request,myid):
    item=Annonce.objects.get(id=myid)
    item.signial+=1
    item.save()
    messages.info(request,'Annonce signalé')
    return redirect(annonce)

def signaler_user(request,myid):
    item=User.objects.get(id=myid)
    item.signial+=1
    item.save()
    messages.info(request,'Utilisateur signalé')
    return redirect(annonce)
@login_required(login_url='../login/')
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
    cagniote = Cagniote.objects.all()
    association = Association.objects.all()
    person = PhysicalUser.objects.all()
    annonce = Annonce.objects.all()
    context= {'cagniote':cagniote.__len__,'association':association.__len__ , 'person':person.__len__ ,'annonce':annonce.__len__}
    return render(request,'admin.html',context)

def Arreter (request,myid) :
    item = Cagniote.objects.get(id =myid)
    item.arret = True
    item.save()
    
    return redirect(ListCagniote)

def Control (request):
    associations1 = Association.objects.all()
    users1 = User.objects.all()
    annonces1 = Annonce.objects.all()

    users = []
    annonces = []
    associations = []

    for i in associations1 :
        if i.is_valid == False   :
            associations.append (i) 

    paginator= Paginator(associations,5)
    page_number2=request.GET.get('page2')
    associations=paginator.get_page(page_number2) 

    for i in users1 :
        if i.signial > 0  :
            users.append (i)  

    paginator= Paginator(users,5)
    page_number1=request.GET.get('page1')
    users=paginator.get_page(page_number1)

    for i in annonces1 :
        if i.signial > 0  :
            annonces.append (i)  

    paginator= Paginator(annonces,5)
    page_number3=request.GET.get('page3')
    annonces=paginator.get_page(page_number3)

    context= {'associations': associations,'users':users, 'annonces':annonces}
    return render(request,'control.html',context)    

def Valider (request,myid) :
    item = Association.objects.get(user_id =myid)
    item.is_valid = True
    item.save()
    SendGmail([item.user.email], "title","confirmation association"," votre association a ete confirmer par administrateur vous pouver maintenant se connecter ")
    
    
    return redirect(Control)

def deleteAssociation (request,myid) :
    item = User.objects.get(id =myid)
    item.delete()
    
    return redirect(Control)

def deleteUser (request,myid) :
    item = User.objects.get(id =myid)
    item.delete()
    
    return redirect(Control)

def deleteAnnonce (request,myid) :
    item = Annonce.objects.get(id =myid)
    item.delete()
    Notification.objects.create(
                user=item.auteur,
                notification="Votre aannonce a etait supprimer par l'administrateur"    
            )

    return redirect(Control)
@login_required(login_url='../login/')
def List_Association (request):
    if 'q' in request.GET :
        q=request.GET['q']
        associations = Association.objects.filter(name__icontains=q)
    else :
        associations = Association.objects.all()
    a= AssociationFilter(request.GET, queryset=associations)
    associations=a.qs
    paginator= Paginator(associations,10)
    page_number=request.GET.get('page')
    associations=paginator.get_page(page_number)
    context= {'associations':associations , "filtre":a}
    return render(request,'listAssociations.html',context)

def Landing(request):
    associations = Association.objects.all()
    cagnottes = Cagniote.objects.all()
    Benevoles = Benevole.objects.all()
    annonce = Annonce.objects.all()

    context= {'associations':associations.__len__ , "cagnottes":cagnottes.__len__ ,"Benevoles":Benevoles.__len__ ,"annonce" :annonce.__len__}

    return render(request,'landing.html' , context)

def landingRecherche(request):
    
    associations = Association.objects.all()
    a= AssociationFilter(request.GET, queryset=associations)
    associations=a.qs
    context= {'associations':associations, 'filtre': a}
    return render(request,'landingRecherche.html',context)

def depotArgent(request,pk):
    form=DepotArgentForm()
    myitem=Cagniote.objects.get(id=pk)
    if request.method =='POST':
        print("here")
        if form.is_valid :
            argent= request.POST['sommeRecolter']
            myitem.sommeRecolter+=float(argent)
            myitem.save()
            return redirect('cagniote')
        else:
            form=DepotArgentForm()
    context={'form':form}
    return render(request,'depotArgent.html',context) 

class ShowProfileBenevole(DetailView):
    model=Benevole
    template_name= 'profilBenevole.html'
    def get_context_data(self, *args,**kwargs):
        profile=Benevole.objects.all()
        context=super(ShowProfileBenevole,self).get_context_data(*args,**kwargs)
        page_user = get_object_or_404(Benevole,id=self.kwargs['pk'])
        context['page_user']=page_user  
        return context
class ShowProfileAnnonce(DetailView):
    model=Annonce
    template_name= 'profilAnnonce.html'
    def get_context_data(self, *args,**kwargs):
        profile=Annonce.objects.all()
        context=super(ShowProfileAnnonce,self).get_context_data(*args,**kwargs)
        page_user = get_object_or_404(Annonce,id=self.kwargs['pk'])
        context['page_user']=page_user  
        return context


@login_required(login_url='../login/')
def ListeBenevole (request):
    benevoles= Benevole.objects.all()
    form = CreateBenevole ()
    local = localisation.objects.all()
    wilaya = localisation.objects.values("wilaya_name").distinct()
    if request.method =='POST':
        username = request.user
        association = Association.objects.get(user=username)
        if form.is_valid :
            titre = request.POST['titre']
            contenu = request.POST['contenu']
            nbr_max = request.POST['nbr_max']
            date = request.POST['date']
            commune = request.POST['commune_name']
            daira = request.POST['daira_name']
            wilaya = request.POST['wilaya_name']
            loc_id = localisation.objects.filter(commune_name__icontains=commune , daira_name__icontains=daira , wilaya_name__icontains=wilaya  )
            print(loc_id)
            print(loc_id)
            type= request.POST['type']
            Benevole.objects.create(
                association = association,
                titre = titre ,
                contenu =contenu ,
                nbr_max = nbr_max ,
                date = date ,
                adresse = loc_id[0],             
                type = type ,
            )

    context= {'form':form , 'benevoles':benevoles , 'local' :local, 'wilaya':wilaya}
    return render(request,'benevole.html',context)

def getNotif(request):
    queryset=Notification.objects.filter(user=request.user)
    return JsonResponse({"notifications":list(queryset.values())})
def ArreterBenevole (request,myid) :
    item = Benevole.objects.get(id =myid)
    item.arret = True
    item.save()
    
    return redirect('profilBenevole.html')
def ajouterPersonne (request,myid) : 
    item = Benevole.objects.get(id =myid)
    item.nbr_actuel = item.nbr_actuel +1
    item.save()

    return redirect('profilBenevole.html')

class Verification(View):
    def get(self,request,uidb64,token):
      return redirect('login.html')

def validerCompte (request,pk):
    item = User.objects.get(email =pk)
    item.is_active = True 
    item.save()
    return redirect('login')

def get_Daira (request):
    wilaya = request.GET.get('wilaya')
    daira = localisation.objects.filter(wilaya_name=wilaya).values('daira_name').distinct()
    context={'daira':daira}
    return render(request,'daira.html',context)
def get_Commune (request):
    daira = request.GET.get('daira')
    commune = localisation.objects.filter(daira_name=daira).values('commune_name').distinct()
    context={'commune':commune}
    return render(request,'commune.html',context) 
