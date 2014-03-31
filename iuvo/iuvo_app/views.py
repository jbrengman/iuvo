from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from iuvo_app.models import User, Event, Contact


def home_view(request):
    context = {}
    return render(request, 'placeholder.html', context)


def login_view(request):
    pass


def register_view(request):
    pass


def dashboard_view(request, user_id):
    pass


def create_event_view(request):
    pass


def edit_event_view(request):
    pass


def create_contact_view(request):
    pass


def edit_contact_view(request):
    pass


def check_in_view(request):
    pass


def about_view(request):
    pass
