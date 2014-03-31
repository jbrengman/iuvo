from django.conf.urls import patterns, url


urlpatterns = patterns(
    'iuvo_app.views',
    url(r'^$', 'home_view', name='home')
)
