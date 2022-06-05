
from xml.dom.pulldom import parseString
from django.shortcuts import  get_object_or_404, redirect, render
from django.http import HttpRequest
from django.contrib.auth import authenticate , login ,logout
from .models import *
from django.core.paginator import Paginator 
from .forms import  *
from django.contrib import messages
from .filters import *
from django.contrib.auth.forms import UserChangeForm ,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views import generic
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
            type = request.POST['type']
            category = request.POST['category']
            
            user = form.save()
            user.is_association =True
            user.save()
            Association.objects.create(
                    user=user ,
                    name=name ,
                    file=file,
                    willaya=willaya,
                    type = type ,
                    category = category,
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
                if  user.is_association   :
                    ass = Association.objects.get(user = user)
                    if ass.is_valid == True :
                        login (request , user ) 
                        return redirect('profile')
                    else :
                        messages.error(request , "cette association n'est pas valide")
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
        elif self.request.user.association == True:
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

def annonce (request):
    annonces= Annonce.objects.all()
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
            Annonce.objects.create(
                auteur = auteur,
                image = image ,
                contenu =contenu ,
                type = type 
            )
            return redirect('annonce')
        else:
            formAnnonce = AnnonceForm()
    commentForm=CommentForm()
    context= {'formAnnonce':formAnnonce , 'annonces':annonces ,'commentForm':commentForm}
    return render(request,'annonce.html',context)

def add_comment (request,myid):
    formComment=CommentForm()
    if request.method == "POST":
        auteur=request.user
        annonce=Annonce.objects.get(id=myid)
        if formComment.is_valid:
            contenu=request.POST['contenu']
            Comment.objects.create(
                auteur=auteur,
                contenu=contenu,
                annonce=annonce
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
    associations = Association.objects.all()
    users = User.objects.all()
    annonces = Annonce.objects.all()

    paginator= Paginator(users,5)
    page_number=request.GET.get('page')
    users=paginator.get_page(page_number)

    paginator= Paginator(associations,5)
    page_number=request.GET.get('page')
    associations=paginator.get_page(page_number)

    paginator= Paginator(annonces,5)
    page_number=request.GET.get('page')
    annonces=paginator.get_page(page_number)

    

    context= {'associations': associations,'users':users, 'annonces':annonces}
    return render(request,'control.html',context)    

def Valider (request,myid) :
    item = Association.objects.get(user_id =myid)
    item.is_valid = True
    item.save()
    
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
    
    return redirect(Control)


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
    return render(request,'landing.html')

def landingRecherche(request):
    return render(request,'landingRecherche.html')

def depotArgent(request):
    return render(request,'depotArgent.html')