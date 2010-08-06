from django import template
from support.forms import ContactForm

register = template.Library()


def show_support_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("support/contact_form.html")(show_contact_form)

def show_support_tab():
    return {}
register.inclusion_tag("support/feedback_tab.html")(show_support_tab)
