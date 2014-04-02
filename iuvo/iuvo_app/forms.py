from django.forms import ModelForm, CharField
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

    class Meta:
        model = Event
        fields = [
            'title', 'location', 'start_day', 'start_time',
            'end_day', 'end_time', 'notify_day', 'notify_time',
            'contacts', 'message']


# This class might be unnecessary
class EditEventForm(ModelForm):

    class Meta:
        model = Event
        fields = []
