from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from iuvo_app.models import Event, Contact
from iuvo_app.forms import ContactForm, EventForm
import datetime


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
    if int(user_id) != request.user.pk:
        raise Http404
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            try:
                event.title = form.cleaned_data.get('title')
                event.location = form.cleaned_data.get('location')
                event.message = form.cleaned_data.get('message')
                event.start_day = form.cleaned_data.get('start_day')
                event.start_time = form.cleaned_data.get('start_time')
                event.end_day = form.cleaned_data.get('end_day')
                event.end_time = form.cleaned_data.get('end_time')
                event.notify_day = form.cleaned_data.get('notify_day')
                event.notify_time = form.cleaned_data.get('notify_time')

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
                        start_date < now or
                        end_date < start_date or
                        notify_date < end_date):
                    raise ValueError  # Change this to a better response

                event.start_date = start_date
                event.end_date = end_date
                event.notify_date = notify_date

                event.save()
                event.contacts = form.cleaned_data.get('contacts')
                event.save()
            except:
                redirect(create_event_view, request.user.pk)  # Add message
            return redirect(view_event_view, request.user.pk, event.pk)
        else:
            return redirect(create_event_view, request.user.pk)  # Add message
    else:
        context = {'event_form': EventForm()}
        return render(request, 'create_event.html', context)


def edit_event_view(request, user_id, event_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        try:
            event.title = form.cleaned_data.get('title')
            event.location = form.cleaned_data.get('location')
            event.message = form.cleaned_data.get('message')
            event.start_day = form.cleaned_data.get('start_day')
            event.start_time = form.cleaned_data.get('start_time')
            event.end_day = form.cleaned_data.get('end_day')
            event.end_time = form.cleaned_data.get('end_time')
            event.notify_day = form.cleaned_data.get('notify_day')
            event.notify_time = form.cleaned_data.get('notify_time')

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
            event.contacts = form.cleaned_data.get('contacts')
            event.save()
        except:
            return redirect(view_event_view, request.user.pk, event.pk)
            # Add error message/handle this better.
        else:
            return redirect(create_event_view, request.user.pk)
            # Add error message/handle this better.
    else:
        context = {'event_form': EventForm(instance=event)}
        return render(request, 'edit_event.html', context)


def contacts_list_view(request, user_id):
    if int(user_id) != request.user.pk:
        raise Http404
    contacts = Contact.objects.filter(owner__pk=user_id)
    context = {'contacts': contacts}
    return render(request, 'contacts_list.html', context)


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
        return render(request, 'create_contact.html', context)


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
        return render(request, 'edit_contact.html', context)


def view_contact_view(request, user_id, contact_id):
    if int(user_id) != request.user.pk:
        raise Http404
    try:
        contact = Contact.objects.get(pk=contact_id)
    except Contact.DoesNotExist:
        raise Http404
    context = {'contact': contact}
    return render(request, 'contact.html', context)


# Helper methods

def get_date(date, time):
    datesplit = date.split('/')
    date_ob = datetime.date(
        int(datesplit[2]), int(datesplit[0]), int(datesplit[1]))
    time_tup = time.split(':')
    time_ob = datetime.time(int(time_tup[0]), int(time_tup[1]))
    date_time = datetime.datetime.combine(date_ob, time_ob)
    return date_time


def clean_num(num):
    import re
    number = re.sub('\D', '', num)
    return number
