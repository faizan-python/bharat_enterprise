from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account
from vendor.models import Vendor


class Payment(models.Model):

    """
    payment model for service
    """
    payment_amount = models.FloatField(default=0)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    recieved_by = models.ForeignKey(User)

    def __unicode__(self):
        return u''.join((self.payment_amount))


class AdvancePayment(models.Model):

    """
    Advance payment model for service
    """
    payment = models.ForeignKey(Payment)
    account = models.ForeignKey(Account)
    vendor = models.ForeignKey(Vendor)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.created_date)


class Item(models.Model):

    """
    Item model
    """
    total_amount = models.FloatField(default=0)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    weight = models.FloatField(default=0)
    price = models.FloatField(default=0)
    item_name = models.CharField(blank=True, null=True, max_length=150)

    def __unicode__(self):
        return u''.join((self.item_name))
