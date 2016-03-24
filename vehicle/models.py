from django.db import models
from django.contrib.auth.models import User

from vendor.models import Vendor


class Vehicle(models.Model):

    """
    Vehicle model to store all Vehicle related information
    """

    vendor = models.ForeignKey(Vendor)
    created_by = models.ForeignKey(User)
    vehicle_number = models.CharField(unique=True, max_length=50)
    vehicle_name = models.CharField(blank=True, max_length=100)
    vehicle_colour = models.CharField(blank=True, max_length=50)
    about = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_visited_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u''.join((self.vehicle_number))
