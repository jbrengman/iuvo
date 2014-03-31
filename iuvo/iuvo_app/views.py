from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from iuvo_app.models import User, Event, Contact


def home_view(request):
    context = {}
    return render(request, 'placeholder.html', context)
