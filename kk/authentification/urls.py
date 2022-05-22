from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('',views.Profile,name='profile'),
    path('login/',views.Loginin,name='login'),
    path('signup/',views.Register,name='signup'),
    path('logout/',views.Logoutt,name='logout'),
    path('createuser/',views.RegisterUser,name='createuser')
]