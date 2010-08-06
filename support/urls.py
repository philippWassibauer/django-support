
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import *


urlpatterns = patterns('',
   url(r'^$',contact_form,name='contact_form'),
   url(r'^modular$', contact_form, {"template_name":"support/modal_form.html"}, name='modular_feedback'),
   url(r'^sent/$', direct_to_template,{ 'template': 'support/contact_form_sent.html' },name='contact_form_sent'),
)
