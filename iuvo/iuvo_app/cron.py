from models import Contact, Event
# from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.template import loader
# from django.template.loader import get_template
from django.template import Context


def send_notifications():
    now = timezone.now()
    events_pre = Event.objects.filter(status=0)
    events_started = Event.objects.filter(status=1)
    events_ended = Event.objects.filter(status=2)

    for event in events_ended:
        if now > event.notify_date:
            # send notification to user's contacts.
            contacts = Contact.objects.filter(owner=event.owner)
            personal_msg = event.message
            # subject = "YOUR FRIEND MAY NEED HELP!!"
            for contact in contacts:
                eddress_list = [contact.email]
                body_template = loader.get_template('notifications/notify_contacts.txt')
                body_context = Context({'msg': personal_msg, 'name': contact.name})
                body = body_template.render(body_context)
                subject_template = loader.get_template('notifications/contacts_email_subject.txt')
                subject_context = Context({})
                subject = subject_template.render(subject_context)
                send_email(eddress_list, subject, body)
            event.status = 3
            event.save()

    for event in events_started:
        if now > event.end_date:
            # send notification to user asking them to check in.
            eddress_list = [event.owner.email]
            # subject = "Iuvo event notice"
            body_template = loader.get_template('notifications/ended.txt')
            body_context = Context({'username': event.owner.username})
            body = body_template.render(body_context)
            subject_template = loader.get_template('notifications/user_email_subject.txt')
            subject_context = Context({})
            subject = subject_template.render(subject_context)
            send_email(eddress_list, subject, body)
            event.status = 2
            event.save()

    for event in events_pre:
        if now > event.start_date:
            # send notification to user telling them that event has started.
            eddress_list = [event.owner.email]
            # subject = "Iuvo event notice"
            body_template = loader.get_template('notifications/started.txt')
            body_context = Context({'username': event.owner.username})
            body = body_template.render(body_context)
            subject_template = loader.get_template('notifications/user_email_subject.txt')
            subject_context = Context({})
            subject = subject_template.render(subject_context)
            send_email(eddress_list, subject, body)
            event.status = 1
            event.save()


def send_3day_notifications():
    now = timezone.now()
    events_notified = Event.objects.filter(status=3)
    events_post_3day = Event.objects.filter(status=4)

    for event in events_post_3day:
        delta = now - event.end_date
        if delta.days % 3 == 0 and delta.days != 0:
            eddress_list = [event.owner.email]
            # subject = "Iuvo event notice"
            body_template = loader.get_template('notifications/late_checkin_email.txt')
            body_context = Context({'username': event.owner.username, 'late': delta.days})
            body = body_template.render(body_context)
            subject_template = loader.get_template('notifications/user_email_subject.txt')
            subject_context = Context({})
            subject = subject_template.render(subject_context)
            send_email(eddress_list, subject, body)

    for event in events_notified:
        delta = now - event.end_date
        delta_min = delta.seconds / 60
        if delta.seconds / 60 > 3:
        # if delta.days > 3:
            eddress_list = [event.owner.email]
            # subject = "Iuvo event notice"
            body_template = loader.get_template('notifications/late_checkin_email.txt')
            body_context = Context({'username': event.owner.username, 'late': delta.days})
            # body_context = Context({'username': event.owner.username, 'late': delta_min})
            body = body_template.render(body_context)
            subject_template = loader.get_template('notifications/user_email_subject.txt')
            subject_context = Context({})
            subject = subject_template.render(subject_context)
            send_email(eddress_list, subject, body)
            event.status = 4
            event.save()


def send_email(recipient_list, subject, body):
    send_mail(subject, body, 'Iuvo Staff <jwhitecf@gmail.com>',
              recipient_list, fail_silently=False)
