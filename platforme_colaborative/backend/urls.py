from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',views.Profile,name='profile'),
    path('login/',views.Login,name='login'),
    path('signup/',views.Register,name='signup'),
]