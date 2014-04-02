from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_str = models.CharField(max_length=15)
    phone_int = models.CharField(blank=True, null=True, max_length=10)
    description = models.TextField(blank=True)  # Might not need this field

    def __unicode__(self):
        return self.name


class Event(models.Model):
    owner = models.ForeignKey(User)
    contacts = models.ManyToManyField(Contact)
    location = models.CharField(max_length=80)
    message = models.TextField(blank=True)
    status = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=80)

    start_day = models.CharField(max_length=15)
    start_time = models.CharField(max_length=15)
    start_date = models.DateTimeField()

    end_day = models.CharField(max_length=15)
    end_time = models.CharField(max_length=15)
    end_date = models.DateTimeField()

    notify_day = models.CharField(max_length=15)
    notify_time = models.CharField(max_length=15)
    notify_date = models.DateTimeField()

    def __unicode__(self):
        return self.owner.username + "'s event ending " + str(self.end_date)
