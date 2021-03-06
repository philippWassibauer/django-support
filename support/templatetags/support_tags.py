from django import template
from support.forms import ContactForm
from support.forms import get_support_moderators as _get_support_moderators

register = template.Library()

def show_support_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("support/contact_form.html")(show_support_form)

def get_support_moderators():
    return _get_support_moderators()
register.simple_tag(get_support_moderators)

def select_support_moderators(ticket):
    return {"moderators": _get_support_moderators(),
            "ticket":ticket}
register.inclusion_tag("support/moderator_select.html")(select_support_moderators)


def get_support_context(context):
    previous_url = ""
    user_agent = ""
    path = ""
    try:
        previous_url = context['request'].META['HTTP_REFERER']
    except:
        pass
    
    try:
        user_agent = context['request'].META['HTTP_USER_AGENT']
    except:
        pass
    
    try:
        path = context['request'].path
    except:
        pass
    
    return {"submission_url": path,
            "previous_url":  previous_url,
            "user_agent": user_agent}
    
    
def show_support_tab(context):
    return get_support_context(context)
register.inclusion_tag("support/feedback_tab.html", takes_context=True)(show_support_tab)

   
def show_support_button(context):
    return get_support_context(context)
register.inclusion_tag("support/feedback_button.html", takes_context=True)(show_support_button)