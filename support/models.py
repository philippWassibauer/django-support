# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from timezones.fields import TimeZoneField
    
class Category(models.Model):
    name = models.CharField(_("name"), max_length=200)
    
    def __unicode__(self):
        return self.name


class SupportQuestion(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_("user"),
                             null=true, blank=true)
    
    category = models.ForeignKey(Category, name=_(u"Category"),
                                            null=True, blank=True)
    
    email = models.EmailField(_(u"email"), max_length=180, null=true, blank=true)
    
    title = models.CharField(_(u"title"), max_length=180, 
                            null=True, blank=True)
    
    message = models.ImageField(upload_to="profile-images", 
                              blank=True, null=True)
    
    submission_date = models.DateTimeField(_(u"submission date"))
    
    class Meta:
        verbose_name = _("support question")
        verbose_name_plural = _("support question")
    
    def __unicode__(self):
        return ""
