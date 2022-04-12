from django.db import models
from django.forms import fields
from .models import UserMaster
from django.forms import ModelForm


class ProfileUpload(ModelForm):
    class Meta:
        model = UserMaster
        fields = '__all__'
