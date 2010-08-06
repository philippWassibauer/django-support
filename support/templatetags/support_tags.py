from django import template
from support.forms import ContactForm

register = template.Library()


def show_contact_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("support/contact_form.html")(show_contact_form)


def show_feedback_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("support/feedback_form.html")(show_feedback_form)
