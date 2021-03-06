from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Defines wether or not a user can log into the admin.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Use this instead of deleting accounts.'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        Or user email address if first and last name are not defined.
        '''
        if (not self.first_name and not self.last_name):
            return '%s' % self.email
        else:
            full_name = '%s %s' % (self.first_name.capitalize(), self.last_name.capitalize())
            return full_name.strip()

    def get_short_name(self):
        '''
        Returns the first name for the user. Or email if none is provided.
        '''
        if (not self.first_name):
            return self.email
        else:
            return self.first_name.capitalize()

    def get_last_name(self):
        '''
        Returns the last name for the user. Or email if none is provided.
        '''
        if (not self.last_name):
            return self.email
        else:
            return self.last_name.capitalize()

    def get_email(self):
        '''
        Returns the user's email address.
        '''
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Group(models.Model):
    name = models.CharField(max_length = 25)
    members = models.ManyToManyField(
        CustomUser
    )

    class Meta:
        verbose_name = "User Group"
        verbose_name_plural = "User Groups"
        ordering = ['name']

    def __str__(self):
        return self.name
