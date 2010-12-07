from django import forms
from django.conf import settings
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _, ugettext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import Permission, User, Group
from models import SupportQuestion

attrs_dict = { 'class': 'required' }

def get_notification_users():
    perm = Group.objects.get(name='moderator')
    users = User.objects.filter(groups=perm)
    return users
    
class ContactForm(forms.ModelForm):
        
    class Meta:
        model = SupportQuestion
        exclude = ("user", "submission_date", "email", "accepted_by", "closed")
    
    def save(self, user, fail_silently=False):
        support_question = super(ContactForm, self).save()
        from_email = user.email
        recipient_list = [user.email for user in get_notification_users()]
        url = "http://%s%s"%(Site.objects.get_current(), reverse("support_moderation"))
        message = render_to_string("emails/support/support_email.txt",
                                   { "user": user,
                                     "url": url,
                                     "support_question": support_question})
        
        send_mail("Kontaktaufnahme von: %(name)s" % {'name': str(user)},
                    message, 
                    from_email, 
                    recipient_list, 
                    fail_silently=True)
        
        return support_question


class AnonymousContactForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AnonymousContactForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True
        
    class Meta:
        model = SupportQuestion
        exclude = ("user", "submission_date", "accepted_by", "closed")
    
    def save(self, fail_silently=False):
        support_question = super(AnonymousContactForm, self).save()
        from_email = self.cleaned_data['email']
        recipient_list = [user.email for user in get_notification_users()]
        url = "http://%s%s"%(Site.objects.get_current(), reverse("support_moderation"))
        message = render_to_string("emails/support/support_email.txt",
                                   {"url": url,
                                     "support_question": support_question})
        send_mail("Kontaktaufnahme von: %(name)s" % {'name': from_email},
                    message, 
                    from_email, 
                    recipient_list, 
                    fail_silently=True)
        
        return support_question
    

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
        
        
        

def get_send_mail():
    """
    A function to return a send_mail function suitable for use in the app. It
    deals with incompatibilities between signatures.
    """
    # favour django-mailer but fall back to django.core.mail
    if "mailer" in settings.INSTALLED_APPS:
        from mailer import send_mail
    else:
        from django.core.mail import send_mail as _send_mail
        def send_mail(*args, **kwargs):
            del kwargs["priority"]
            return _send_mail(*args, **kwargs)
    return send_mail

send_mail = get_send_mail()

