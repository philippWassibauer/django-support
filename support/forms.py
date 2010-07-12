from django import forms
from django.conf import settings
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _, ugettext

from misc.utils import get_send_mail
send_mail = get_send_mail()


attrs_dict = { 'class': 'required' }


class ContactForm(forms.Form):
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict),label=_("Your name"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)),label=_("Your email address"))
    message = forms.CharField(widget=forms.Textarea(attrs=attrs_dict), label=_("Your message"))
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    
    def save(self, fail_silently=False):
        send_mail("Kontaktaufnahme von: %(name)s" % {'name': self.cleaned_data['name']},
                    self.cleaned_data['message'], 
                    self.cleaned_data['email'], 
                    self.recipient_list, 
                    fail_silently=True)


class AkismetContactForm(ContactForm):
    def clean_body(self):
        if 'body' in self.cleaned_data and getattr(settings, 'AKISMET_API_KEY', ''):
            from akismet import Akismet
            from django.utils.encoding import smart_str
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                  blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referer': self.request.META.get('HTTP_REFERER', ''),
                                 'user_ip': self.request.META.get('REMOTE_ADDR', ''),
                                 'user_agent': self.request.META.get('HTTP_USER_AGENT', '') }
                if akismet_api.comment_check(smart_str(self.cleaned_data['body']), data=akismet_data, build_data=True):
                    raise forms.ValidationError(u"Akismet thinks this message is spam")
        return self.cleaned_data['body']
