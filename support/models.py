# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from timezones.fields import TimeZoneField
from datetime import datetime

SUPPORT_CHOICES = (
    ('feedback', _(u'Feedback')),
    ('bug', _(u'Bug')),
    ('feature', _(u'Feature')),
    ('complaint', _(u'Complaint')),
)


class SupportQuestion(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"),
                             null=True, blank=True)
    
    category = models.CharField(_(u"Category"), max_length=180, 
                            null=True, blank=True, choices=SUPPORT_CHOICES)
    
    email = models.EmailField(_(u"email"), blank=True)
    
    title = models.CharField(_(u"title"), max_length=180, 
                            null=True, blank=True)
    
    message = models.TextField(_(u"question"))
    
    submission_date = models.DateTimeField(_(u"submission date"), default=datetime.now)
    
    accepted_by = models.ForeignKey(User, verbose_name=_("user"),
                             null=True, blank=True, related_name="accepted_tickets")
    closed = models.BooleanField(_(u"closed"))
    
    class Meta:
        verbose_name = _("support question")
        verbose_name_plural = _("support question")
    
    def __unicode__(self):
        return ""
