from django.conf.urls import patterns, include, url
from django.contrib import admin
# from iuvo_app.forms import RegisterForm
# import iuvo_app.urls
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('iuvo_app.urls')),
    url(r'^accounts/',
        include('registration.backends.default.urls')),
    # url(r'^accounts/$',
    #     register,
    #     {'backend': 'registration.backends.default.DefaultBackend',
    #     'form_class': RegisterForm})
)


# (r'^register/$',
#     register,
#     {'backend': 'registration.backends.default.DefaultBackend',
#      'form_class': MyExtendedForm}),