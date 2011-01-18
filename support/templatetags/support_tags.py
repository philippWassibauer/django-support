from django import template
from support.forms import ContactForm

register = template.Library()


def show_support_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("support/contact_form.html")(show_support_form)

def show_support_tab(context):
    previous_url = ""
    user_agent = ""
    try:
        previous_url = context['request'].META['HTTP_REFERER']
    except:
        pass
    
    try:
        user_agent = context['request'].META['HTTP_USER_AGENT']
    except:
        pass
    
    return {"submission_url": context['request'].path,
            "previous_url":  previous_url,
            "user_agent": user_agent}
register.inclusion_tag("support/feedback_tab.html", takes_context=True)(show_support_tab)
