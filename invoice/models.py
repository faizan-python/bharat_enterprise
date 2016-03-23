from django.db import models
from django.contrib.auth.models import User

from company.models import Company
from payment.models import (
    Payment,
    Item
)
from vendor.models import Vendor
from vehicle.models import (
    Vehicle
)


class Invoice(models.Model):

    """
    Invoice model to store all service related information
    """

    company = models.ForeignKey(Company)
    vendor = models.ForeignKey(Vendor)
    created_by = models.ForeignKey(User)
    vehicle = models.ForeignKey(Vehicle, blank=True, null=True)
    payment = models.ManyToManyField(Payment)
    item = models.ManyToManyField(Item)
    remark = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    total_paid = models.FloatField(default=0)
    total_pending = models.FloatField(default=0)
    invoice_number = models.AutoField(primary_key=True)
    advance_payment = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)
    total_weight = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_archive = models.BooleanField(default=False)
    complete_payment = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.invoice_number)
