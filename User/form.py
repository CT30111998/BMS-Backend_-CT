from django.db import models
from django.forms import fields
from .models import User
from django.forms import ModelForm

class profileUpload(ModelForm):
    class meta:
        model = User
        fields = '__all__'