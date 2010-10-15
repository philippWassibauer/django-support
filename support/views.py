"""
View which can render and send email from a contact form.

"""

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import ContactForm, AnonymousContactForm


def contact_form(request, form_class=ContactForm,
                 template_name='support/contact_form.html',
                 success_url=None, extra_context=None,
                 fail_silently=False):
    
    if not request.user.is_authenticated():
        form_class = AnonymousContactForm
        
    if success_url is None:
        success_url = reverse('contact_form_sent')
        
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            if request.user.is_authenticated():
                support_question = form.save(request.user, fail_silently=fail_silently)
            else:
                support_question = form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
        
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'contact_form': form },
                              context_instance=context)
