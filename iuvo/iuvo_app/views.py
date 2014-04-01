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


def about_view(request):
    pass


def dashboard_view(request, user_id):
    pass


def check_in_view(request, user_id, event_id):
    pass


def events_list_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    events = Event.objects.filter(owner__pk=user_id)
    context = {'events': events, 'title': 'All events'}
    return render(request, 'events_list.html', context)


def events_upcoming_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    events = Event.objects.filter(owner__pk=user_id, status=0)
    context = {'events': events, 'title': 'Upcoming events'}
    return render(request, 'events_list.html', context)


def events_current_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    events = Event.objects.filter(owner__pk=user_id, status__gte=1)
    context = {'events': events, 'title': 'Ongoing events'}
    return render(request, 'events_list.html', context)


def events_past_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    events = Event.objects.filter(owner__pk=user_id).filter(status=-1)
    context = {'events': events, 'title': 'Past events'}
    return render(request, 'events_list.html', context)


def view_event_view(request, user_id, event_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404
    context = {'event': event}
    return render(request, 'event.html', context)


def create_event_view(request, user_id):
    pass


def edit_event_view(request, user_id, event_id):
    pass


def contacts_list_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    contacts = Contact.objects.filter(owner__pk=user_id)
    context = {'contacts': contacts}
    return render(request, 'contacts_list.html', context)


def create_contact_view(request, user_id):
    pass


def view_contact_view(request, user_id, contact_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        contact = Contact.objects.get(pk=contact_id)
    except Contact.DoesNotExist:
        raise Http404
    context = {'contact': contact}
    return render(request, 'contact.html', context)


def edit_contact_view(request, user_id, contact_id):
    pass
