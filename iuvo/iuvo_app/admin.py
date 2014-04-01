from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from django.core.urlresolvers import reverse
from iuvo_app.models import Contact, Event


class ContactInLineAdmin(admin.TabularInline):
    model = Event.contacts.through
    extra = 1


class ContactAdmin(admin.ModelAdmin):

    inlines = [ContactInLineAdmin, ]

    list_display = (
        '__unicode__', 'email', 'phone_str', 'description', 'owner_link')

    def owner_link(self, contact):
        url = reverse('admin:auth_user_change', args=(contact.owner.pk, ))
        name = contact.owner.username
        return '<a href="%s">%s</a>' % (url, name)

    owner_link.allow_tags = True
    owner_link.short_description = 'Contact creator'


class EventAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__',  'start_date', 'end_date', 'notify_date',
        'status', 'owner_link')

    def owner_link(self, event):
        url = reverse('admin:auth_user_change', args=(event.owner.pk, ))
        name = event.owner.username
        return '<a href="%s">%s</a>' % (url, name)

    owner_link.allow_tags = True
    owner_link.short_description = 'Event creator'


admin.site.register(Contact, ContactAdmin)
admin.site.register(Event, EventAdmin)
>>>>>>> jordan
