
from dataclasses import field
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , PasswordChangeForm
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
    # image=forms.ImageField(widget=)
    class Meta:
        model=Annonce
        fields=['contenu','image','type']
        widgets={
            'contenu':forms.Textarea(attrs={'class':'textholder','placeholder':'ecrire ...'}),
            'image':forms.widgets.FileInput(attrs={'id':'image_input'}),
            'type':forms.Select(attrs={'class':'input'})
        }

class CommentForm (ModelForm):
    class Meta:
        model=Comment
        fields=['contenu']
        widgets={
            'contenu':forms.TextInput(attrs={'class':'form-control','placeholder':'Ajouter un comentaire'}),
        }
            
class CreateCagniote (forms.ModelForm):
    class Meta:
        model= Cagniote
        fields=["titre","contenu","sommeDemander"]

class EditProfileForm(UserChangeForm):

    class Meta:
        model =User
        fields=['username','email','phone','img']
        labels = {
            "username": "",
            "email":"",
            "phone":"",
            "img":""
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'input','placeholder':'Username'}),
            'email':forms.EmailInput(attrs={'class':'input','placeholder':'Email'}),
            'phone':forms.NumberInput(attrs={'class':'input','placeholder':'Phone number'}),
        }
            
class PasswordForm(PasswordChangeForm):
    old_password: forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','type':'password'}))
    class Meta:
        model=User
class CreateBenevole (forms.ModelForm):
    class Meta:
        model= Benevole
        fields=["titre","contenu","adresse","type","nbr_max"]

