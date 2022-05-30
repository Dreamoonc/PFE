from django.db.models import fields
from django.forms.widgets import *
import django_filters
from django_filters import *
from .models import *


class AssociationFilter(django_filters.FilterSet):

    class  Meta :
       model = Association
       fields = '__all__'