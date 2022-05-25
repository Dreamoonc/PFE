from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('',views.Profile,name='profile'),
    path('annonce/',views.annonce,name='annonce'),
    path('login/',views.Loginin,name='login'),
    path('signup/',views.Register,name='signup'),
    path('logout/',views.Logoutt,name='logout'),
    path('createuser/',views.RegisterUser,name='createuser'),
    path('select/',views.Select,name='select'),
    path('cagniote/',views.ListCagniote,name='cagniote'),
     path('delete_annonce/<str:myid>/',delete_annonce,name='delete_annonce'),
]