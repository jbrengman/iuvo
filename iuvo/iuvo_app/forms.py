from django.forms import ModelForm, DateTimeField, CharField
from bootstrap3_datetime.widgets import DateTimePicker
from iuvo_app.models import Event, Contact


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_str', 'description']


# This class might be unnecessary
class EditContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = []


class EventForm(ModelForm):

    # start_day = DateTimeField(widget=DateTimePicker(
    #     options={'pickTime': False, 'format': 'MM-DD-YYYY'}))
    # start_time = DateTimeField(widget=DateTimePicker(
    #     options={'format': 'HH:mm A/PM', 'pickDate': False, 'pick12HourFormat': False, 'pickSeconds': False}))

    # end_day = DateTimeField(widget=DateTimePicker(
    #     options={'pickTime': False, 'format': 'MM-DD-YYYY'}))
    # end_time = DateTimeField(widget=DateTimePicker(
    #     options={'format': 'HH:mm', 'pickDate': False, 'pick12HourFormat': True, 'pickSeconds': False, 'minuteStepping': 15}))

    # notify_day = DateTimeField(widget=DateTimePicker(
    #     options={'pickTime': False, 'format': 'MM-DD-YYYY'}))
    # notify_time = DateTimeField(widget=DateTimePicker(
    #     options={'format': 'HH:mm', 'pickDate': False, 'pickSeconds': False, 'minuteStepping': 15}))

    start_time = CharField()
    end_time = CharField()
    notify_time = CharField()

    class Meta:
        model = Event
        fields = [
            'title', 'location', 'start_date', 'start_time',
            'end_date', 'end_time', 'notify_date', 'notify_time',
            'contacts', 'message']


# This class might be unnecessary
class EditEventForm(ModelForm):

    class Meta:
        model = Event
        fields = []
