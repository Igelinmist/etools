from django.contrib.auth.models import User
from django.db import models

# from .journal_models import Equipment


class Employee(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    department = models.CharField(max_length=100)
    equipment = models.ForeignKey('Equipment')
