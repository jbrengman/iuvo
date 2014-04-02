from models import Contact, Event
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail


def send_notifications():
    now = timezone.now()
    events_pre = Event.objects.filter(status=0)
    events_started = Event.objects.filter(status=1)
    events_ended = Event.objects.filter(status=2)

    for event in events_ended:
        if now > event.notify_date:
            # send notification to user's contacts.
            contacts = Contact.objects.filter(owner=event.owner)
            eddress_list = []
            for contact in contacts:
                eddress_list.append(contact.email)
            subject = "YOUR FRIEND MAY NEED HELP!!"
            body = """You are receiving this email, because a friend has assigned
                      you as an emergency contact at Iuvo.com.  They have scheduled an
                      event which is past its end time, and they have not checked in.
                      Please try to contact your friend to see if they are safe.  Thank you.

                      Regards,
                      Iuvo Staff"""
            send_email(eddress_list, subject, body)
            event.status = 3
            event.save()

    for event in events_started:
        if now > event.end_date:
            # send notification to user asking them to check in.
            eddress_list = [event.owner.email]
            subject = "Iuvo event notice"
            body = """The event which you've scheduled at Iuvo.com has ended.
                      Please, log into Iuvo.com and submit a check-in for your event.

                      Regards,
                      Iuvo Staff"""
            send_email(eddress_list, subject, body)
            event.status = 2
            event.save()

    for event in events_pre:
        if now > event.start_date:
            # send notification to user telling them that event has started.
            eddress = [event.owner.email]
            subject = "Iuvo event notice"
            body = """The event which you've scheduled at Iuvo.com has started.
                      If you've canceled your plans, Please log into your account
                      and cancel the event.

                      Regards,
                      Iuvo Staff"""
            send_email(eddress, subject, body)
            event.status = 1
            event.save()


def send_3day_notifications():
    now = timezone.now()
    events_notified = Event.objects.filter(status=3)
    events_post_3day = Event.objects.filter(status=4)

    for event in events_post_3day:
        delta = now - event.end_date
        if delta.days % 3 == 0:
            eddress_list = [event.owner.email]
            subject = "Iuvo event notice"
            body = """You had scheduled an event at Iuvo.com.  It is now 3 days past
                      the end time for this event.  Please, log into your account and
                      check-in or your account will be suspended.  Thank you.

                      Regards,
                      Iuvo Staff"""
            send_email(eddress_list, subject, body)

    for event in events_notified:
        delta = now - event.end_date
        # if delta.seconds / 60 > 3:
        if delta.days > 3:
            eddress_list = [event.owner.email]
            subject = "Iuvo event notice"
            body = """You had scheduled an event at Iuvo.com.  It is now 3 days past
                      the end time for this event.  Please, log into your account and
                      check-in or your account will be suspended.  Thank you.

                      Regards,
                      Iuvo Staff"""
            send_email(eddress_list, subject, body)
            event.status = 4
            event.save()


def send_email(recipient_list, subject, body):
    send_mail(subject, body, 'jwhitecf@gmail.com',
              recipient_list, fail_silently=False)
