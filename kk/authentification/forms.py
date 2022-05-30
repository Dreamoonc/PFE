from tkinter import Widget
from django import forms
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate 

class CreateUserForm (UserCreationForm):
    class Meta :
        model = User
        fields = ["username" ,"email","phone" ,'password1','password2']


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="password",widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=["email","password"]
    
    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password = self.cleaned_data['password']    

            if not authenticate (email=email , password=password):
                raise forms.ValidationError("email or password incorrect ")



class CreateAssociation (forms.ModelForm):
     class Meta:
        model=Association
        fields=["name","file","willaya","type","category"]

class CreatePersonne (forms.ModelForm):
     class Meta:
        model=PhysicalUser
        fields=["first_name","last_name","willaya"]

class AnnonceForm (ModelForm):
    class Meta:
        model=Annonce
        fields=['contenu','image','type']
        # widgets={
        #     'Contenu': TextInput()
        #     'NivEtude'
        # }
        widgets={
            'contenu':forms.Textarea(attrs={'class':'textholder','placeholder':'ecrire ...'})
        }

            
class CreateCagniote (forms.ModelForm):
    class Meta:
        model= Cagniote
        fields=["titre","contenu","sommeDemander"]

