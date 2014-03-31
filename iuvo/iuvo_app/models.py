from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    owner = models.ForeignKey(User)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    phone_str = models.CharField(max_length=15)
    phone_int = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)  # Might not need this field


class Event(models.Model):
    owner = models.ForeignKey(User)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    notify_date = models.DateTimeField()  # Default to equal end_date
    contacts = models.ManyToManyField(Contact)
    location = name = models.CharField(max_length=80)
    message = models.TextField(blank=True)
    status = models.CharField()
