from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class UserProfile(models.Model):

    """
    UserProfile model
    """

    class Gender(Enum):

        """
        This class creates enum for gender field of UserProfile.
        """

        MALE = 'Male'
        FEMALE = 'Female'

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    designation = models.CharField(blank=True, max_length=120)
    company_name = models.CharField(blank=True, max_length=120)
    about = models.TextField(blank=True, null=True)
    gender = models.CharField(blank=True, max_length=20,
                              choices=Gender.as_tuple())
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=50)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u' '.join((self.first_name, self.last_name))


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance=None,
                            created=False, **kwargs):
    """
    When a new user is created this fuctions creates a userprofile
    for that particular user.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def delete_profile_for_user(sender, instance=None, **kwargs):
    """
    When a user is deleted this fuctions deletes the userprofile
    of that particular user.
    """
    if instance:
        user_profile = UserProfile.objects.get(user=instance)
        user_profile.delete()
