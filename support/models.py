# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
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
    
    email = models.EmailField(_(u"Email"), blank=True)
    
    title = models.CharField(_(u"Title"), max_length=180, 
                            null=True, blank=True)
    
    message = models.TextField(_(u"Question"))
    
    submission_date = models.DateTimeField(_(u"Submission date"), default=datetime.now)
    
    accepted_by = models.ForeignKey(User, verbose_name=_("User"),
                             null=True, blank=True, related_name="accepted_tickets")
    closed = models.BooleanField(_(u"Closed"))
    
    # Metadata
    user_agent = models.CharField(max_length=380, null=True, blank=True)
    submission_url = models.CharField(max_length=280, null=True, blank=True)
    previous_url = models.CharField(max_length=280, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Support question")
        verbose_name_plural = _("Support question")
        ordering = ("submission_date",)
        
    def __unicode__(self):
        return "%s > %s (%s)"%(self.user, self.title, self.get_category_display())
