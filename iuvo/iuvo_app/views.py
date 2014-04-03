from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from iuvo_app.models import Event, Contact
from iuvo_app.forms import ContactForm, EventForm
import datetime
import pytz
from django.utils import timezone


def home_view(request):
    context = {}
    return render(request, 'iuvo_app/homepage.html', context)


def login_view(request):
    login_form = LoginFxorm()
    context = {'form': login_form}
    return render(request, 'registration/login.html', context)


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
    upcoming_events = Event.objects.filter(owner__pk=user_id, status=0)
    ongoing_events = Event.objects.filter(owner__pk=user_id, status__gte=1)
    past_events = Event.objects.filter(owner__pk=user_id).filter(status=-1)
    context = {'upcoming_events': upcoming_events,
               'ongoing_events': ongoing_events,
               'past_events': past_events,
               'title': 'Your events'}
    return render(request, 'iuvo_app/events_list.html', context)


def events_upcoming_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    upcoming_events = Event.objects.filter(owner__pk=user_id, status=0)
    context = {'upcoming_events': upcoming_events, 'title': 'Upcoming events'}
    return render(request, 'iuvo_app/events_list.html', context)


def events_current_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    ongoing_events = Event.objects.filter(owner__pk=user_id, status__gte=1)
    context = {'ongoing_events': ongoing_events, 'title': 'Ongoing events'}
    return render(request, 'iuvo_app/events_list.html', context)


def events_past_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    past_events = Event.objects.filter(owner__pk=user_id).filter(status=-1)
    context = {'past_events': past_events, 'title': 'Past events'}
    return render(request, 'iuvo_app/events_list.html', context)


def view_event_view(request, user_id, event_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404
    context = {'event': event}
    return render(request, 'iuvo_app/event.html', context)


def create_event_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.title = form.cleaned_data.get('title')
            event.location = form.cleaned_data.get('location')
            event.message = form.cleaned_data.get('message')
            event.start_day = form.cleaned_data.get('start_day')
            event.start_time = form.cleaned_data.get('start_time')
            event.end_day = form.cleaned_data.get('end_day')
            event.end_time = form.cleaned_data.get('end_time')
            event.notify_day = form.cleaned_data.get('notify_day')
            event.notify_time = form.cleaned_data.get('notify_time')
            tz = form.cleaned_data.get('timezone')

            start_date = get_date(
                form.cleaned_data.get('start_day'),
                form.cleaned_data.get('start_time'),
                tz)
            end_date = get_date(
                form.cleaned_data.get('end_day'),
                form.cleaned_data.get('end_time'),
                tz)
            notify_date = get_date(
                form.cleaned_data.get('notify_day'),
                form.cleaned_data.get('notify_time'),
                tz)

            now = timezone.now()
            if (  # Checking for appropriate dates.
                    start_date < now or
                    end_date < start_date or
                    notify_date < end_date):
                raise ValueError  # Change this to a better response

            event.start_date = start_date
            event.end_date = end_date
            event.notify_date = notify_date

            event.status = 0

            event.save()
            event.contacts = form.cleaned_data.get('contacts')
            event.save()
            return redirect(view_event_view, request.user.pk, event.pk)
        else:
            return redirect(create_event_view, request.user.pk)  # Add message
    else:
        context = {'event_form': EventForm()}
        return render(request, 'iuvo_app/create_event.html', context)


def edit_event_view(request, user_id, event_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            # event.title = form.cleaned_data.get('title')
            # event.location = form.cleaned_data.get('location')
            # event.message = form.cleaned_data.get('message')
            # event.start_day = form.cleaned_data.get('start_day')
            # event.start_time = form.cleaned_data.get('start_time')
            # event.end_day = form.cleaned_data.get('end_day')
            # event.end_time = form.cleaned_data.get('end_time')
            # event.notify_day = form.cleaned_data.get('notify_day')
            # event.notify_time = form.cleaned_data.get('notify_time')
            event = form.save(commit=False)
            start_date = get_date(
                form.cleaned_data.get('start_day'),
                form.cleaned_data.get('start_time'))
            end_date = get_date(
                form.cleaned_data.get('end_day'),
                form.cleaned_data.get('end_time'))
            notify_date = get_date(
                form.cleaned_data.get('notify_day'),
                form.cleaned_data.get('notify_time'))

            now = datetime.datetime.now()
            if (  # Checking for appropriate dates.
                    end_date < now or
                    notify_date < end_date):
                raise ValueError  # Change this to a better response

            event.start_date = start_date
            event.end_date = end_date
            event.notify_date = notify_date

            event.save()
            form.save_m2m()
            # event.contacts = form.cleaned_data.get('contacts')
            # event.save()
            return redirect(events_list_view, request.user.pk)
        else:
            return redirect(edit_event_view, request.user.pk, event.pk)
            # Add error message/handle this better.
    else:
        context = {'event_form': EventForm(instance=event), 'event': event}
        return render(request, 'iuvo_app/edit_event.html', context)


def contacts_list_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    contacts = Contact.objects.filter(owner__pk=user_id)
    context = {'contacts': contacts}
    return render(request, 'iuvo_app/contacts_list.html', context)


def create_contact_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    if request.method == 'POST':
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                contact = form.save(commit=False)
                contact.owner = request.user
                contact.name = form.cleaned_data.get('name')
                contact.email = form.cleaned_data.get('email')
                contact.phone_str = form.cleaned_data.get('phone_str')
                contact.phone_int = clean_num(
                    form.cleaned_data.get('phone_str'))
                contact.description = form.cleaned_data.get('description')
                contact.save()
                return redirect(view_contact_view, request.user.pk, contact.pk)
            else:
                return redirect(create_contact_view, request.user.pk)
        except:
            return redirect(create_contact_view, request.user.pk)
    else:
        context = {'contact_form': ContactForm()}
        return render(request, 'iuvo_app/create_contact.html', context)


def edit_contact_view(request, user_id, contact_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        contact = Contact.objects.get(pk=contact_id)
        if contact.owner.pk != request.user.pk:
            raise Http404
    except Contact.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact.name = form.cleaned_data.get('name')
            contact.email = form.cleaned_data.get('email')
            contact.phone_str = form.cleaned_data.get('phone_str')
            contact.phone_int = clean_num(form.cleaned_data.get('phone_str'))
            contact.description = form.cleaned_data.get('description')
            contact.save()
            return redirect(view_contact_view, request.user.pk, contact.pk)
        else:
            return redirect(edit_event_view, request.user.pk, contact_id)
    else:
        contact_form = ContactForm(instance=contact)
        context = {'contact_form': contact_form, 'contact_id': contact_id}
        return render(request, 'iuvo_app/edit_contact.html', context)


def view_contact_view(request, user_id, contact_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        contact = Contact.objects.get(pk=contact_id)
    except Contact.DoesNotExist:
        raise Http404
    context = {'contact': contact}
    return render(request, 'iuvo_app/contact.html', context)


# Helper methods

def get_date(date, time, timezone):
    tz = pytz.timezone(timezone)
    datesplit = date.split('/')
    date_ob = datetime.date(
        int(datesplit[2]), int(datesplit[0]), int(datesplit[1]))
    time_tup = time.split(':')
    time_ob = datetime.time(int(time_tup[0]), int(time_tup[1]), tzinfo=tz)
    date_time = datetime.datetime.combine(date_ob, time_ob)
    return date_time


def clean_num(num):
    import re
    number = re.sub('\D', '', num)
    return number
