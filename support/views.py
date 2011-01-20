"""
View which can render and send email from a contact form.

"""
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from forms import ContactForm, AnonymousContactForm
from models import SupportQuestion, SupportReply
from django.contrib.auth.models import User
from misc.html_email import send_html_email

def contact_form_moderate(request, template_name="support/moderate.html"):
    open_tickets = SupportQuestion.objects.filter(closed=False)
    unaccepted_tickets = SupportQuestion.objects.filter(accepted_by__isnull=True)
    tickets = SupportQuestion.objects.all()
    your_tickets = SupportQuestion.objects.filter(accepted_by=request.user)
    return render_to_response(template_name,
                              {
                                "open_tickets": open_tickets,
                                "unaccepted_tickets": unaccepted_tickets,
                                "tickets": tickets,
                                "your_tickets": your_tickets,
                              },
                              context_instance=RequestContext(request))
    
   
def view_ticket(request, id, template_name="support/ticket.html"):
    ticket = SupportQuestion.objects.get(pk=id)
    return render_to_response(template_name,
                              { 'ticket': ticket },
                              context_instance=RequestContext(request))
    
def edit_ticket(request, id,  template_name=""):
    ticket = SupportQuestion.objects.get(pk=id)
    if request.POST:
        # check if it is assigned
        if request.POST.get("action")=="assign":
            ticket.accepted_by = User.objects.get(pk=request.POST.get("assign-to"))
            send_html_email([ticket.accepted_by.email], "emails/support_ticket_assigned", {"ticket": ticket})
            messages.success(request, _("Ticket has been assigned"))
            
        # check if it is closed or reopened
        if request.POST.get("action")=="close":
            ticket.closed = True
            messages.success(request, _("Ticket was closed"))
        
        if request.POST.get("action")=="open":
            ticket.closed = False
            messages.success(request, _("Ticket was reopened"))
        
        # check for reply
        if request.POST.get("action")=="reply":
            message = request.POST.get("message")
            reply = SupportReply(message=message, user=request.user,
                         support_question=ticket)
            reply.save()
            
            email = ticket.email
            if ticket.user:
                email = ticket.user.email
            send_html_email([email], "emails/support_ticket_reply", {"ticket": ticket,
                                                                     "reply":reply})
            messages.success(request, _("Ticket reply has been sent"))
            
        # save
        ticket.save()
        return HttpResponseRedirect(reverse('support_view_ticket', args=(ticket.pk,)))
        
    return render_to_response(template_name,
                              { 'ticket': ticket },
                              context_instance=RequestContext(request))
    
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
        form = form_class(initial=request.GET)
        

    if extra_context is None:
        extra_context = {}
        
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'contact_form': form },
                              context_instance=context)
