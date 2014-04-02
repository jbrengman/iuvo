from django.forms import ModelForm  # , ModelMultipleChoiceField
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
            'name', 'location', 'start_date', 'end_date',
            'notify_date', 'contacts', 'message']


# This class might be unnecessary
class EditEventForm(ModelForm):

    class Meta:
        model = Event
        fields = []
