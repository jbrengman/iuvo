from models import Contact, Event
from django.contrib.auth.models import User


def test():
    print('test')


def test_user_query():
    user = User.objects.get(id=1)
    print(user.username)


def test_contact_create():
    user = User.objects.get(id=1)
    Contact.objects.create(owner=user, email='tester@gmail.com',
                           name='tester', phone_str='5555555555')


def status_change_test():
    event = Event.objects.get(id=5)
    # if event is None:
    #     user = User.objects.get(id=1)
    #     contact = Contact.objects.get(name='tester')
    #     Event.objects.create(owner=user, contacts=contact, location='here')
    if event.status is None:
        event.status = 1
        event.save()
    elif event.status == 1:
        event.status = 2
        event.save()
    elif event.status == 2:
        event.status = 3
        event.save()
    elif event.status == 3:
        event.status = 4
        event.save()
    else:
        pass
