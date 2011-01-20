
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import *


urlpatterns = patterns('',
   url(r'^$',contact_form,name='support'),
   url(r'^edit/(?P<id>[\d]+)$', edit_ticket, name='support_edit_ticket'),
   url(r'^moderate/$',contact_form_moderate,name='support_moderation'),
   url(r'^modular$', contact_form, {"template_name":"support/modal_form.html"}, name='modular_feedback'),
   url(r'^success/$', direct_to_template, { 'template': 'support/contact_form_sent.html' },name='contact_form_sent'),
)
