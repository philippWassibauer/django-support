
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import contact_form


urlpatterns = patterns('',
   url(r'^$',contact_form,name='contact_form'),
   url(r'^sent/$', direct_to_template,{ 'template': 'support/contact_form_sent.html' },name='contact_form_sent'),
)
