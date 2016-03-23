from django.db import models
from django.contrib.auth.models import User

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
        return str(self.payment_amount)


class Item(models.Model):

    """
    Item model
    """
    payment_amount = models.FloatField(default=0)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    weight = models.FloatField(default=0)
    item_name = models.CharField(blank=True, null=True, max_length=150)

    def __unicode__(self):
        return str(self.name)
