from django.db import models

from django.contrib.auth.models import User
from accounts.models import Account


class Vendor(models.Model):

    """
    Vendor model to store all Vendor related information
    """

    account = models.ForeignKey(Account)
    created_by = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    contact_person = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u''.join((self.name))
