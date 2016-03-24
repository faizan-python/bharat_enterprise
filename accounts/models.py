from django.db import models

from django.contrib.auth.models import User


class Plans(models.Model):
    """
    Base Class capturing all plans information
    that provider can buy.
    """
    plan_type = models.CharField(max_length=50)
    price = models.FloatField()
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='plans_created_by')
    updated_by = models.ForeignKey(
            User, blank=True, null=True, related_name='plans_modified_by')
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return u''.join((self.plan_type))


class Account(models.Model):
    """
    Base class for storing customer related information
    Customers are basically clients that purchase plans from audetemi
    Every customer will have one user account
    One admin who is goint to add agent system
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=70)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    plans = models.ForeignKey(Plans, null=True, blank=True)
    plan_start_date = models.DateTimeField(auto_now_add=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    updated_by = models.ForeignKey(
            User, blank=True, null=True, related_name='org_modified_by')

    def __unicode__(self):
        return u''.join((self.name))
