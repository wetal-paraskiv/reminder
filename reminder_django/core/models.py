from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.db import models

from django import forms
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.utils.timezone import datetime, timedelta
import pytz
local_tz = pytz.timezone('UTC')  # offset-aware datetime



REMINDER_LEN = 100

def validate_reminder_length(value):
    if len(value) > REMINDER_LEN:
        raise ValidationError(
            _('%(value)s is too long..'),
            params={'value': value},
        )


class Reminder(models.Model):

    REPEAT_CHOICES = [
        ('0', 'no repeat'),
        ('600', '10 minutes'),
        ('900', '15 minutes'),
        ('1800', '30 minutes'),
        ('3600', '1 hour'),
        ('10800', '3 hours'),
        ('21600', '6 hours'),
        ('86400', '1 day'),
        ('259200', '3 days'),
        ('604800', '7 days'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(
        max_length=100, verbose_name=" remind me to..", validators=[validate_reminder_length])
    date = models.DateTimeField(verbose_name=' set time alarm')
    repeat = models.CharField(
        max_length=10, choices=REPEAT_CHOICES, default='default', verbose_name=" repeat interval")
    active = models.BooleanField(
        default=True, verbose_name=" active")

    def __str__(self):
        return self.text

    # tells django where to go when new instance is created
    def get_absolute_url(self):
        return reverse('core:active')

