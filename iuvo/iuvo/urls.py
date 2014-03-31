from django.conf.urls import patterns, include, url
from django.contrib import admin
import iuvo_app.urls
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(iuvo_app.urls))
)
