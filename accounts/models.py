from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Not specified', 'Not Specified'),
)

IS_ACTIVE_CHOICES = (
    (True, 'Active'),
    (False, 'Inactive'),
)


class UserProfile(models.Model):
    """Model to add a profile to user."""

    user = models.OneToOneField(User)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='Not specified')
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=8, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
