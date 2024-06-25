from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.email}"
    
    def get_short_name(self):
        return self.first_name
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ["last_name"]

class Profile(models.Model):
    """
    Model to represent extended auth User Class to add additional
    profile information.
    """
    class PreferredCommunicationChoices(models.TextChoices):
        EMAIL = 'EMAIL', _('Email')
        PHONE = 'PHONE', _('Phone')
        MAIL= 'MAIL', _('Mail')

    class LanguageChoices(models.TextChoices):
        EN = "en", _("English")
        ES = "es", _("Spanish")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=25, choices=LanguageChoices.choices, default=LanguageChoices.EN, verbose_name=_('Preferred Language'))
    additional_phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], null=True, blank=True, verbose_name=_('Additional Phone Number'))
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Emergency Contact Name'))
    emergency_contact_phone = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], null=True, blank=True, verbose_name=_('Emergency Contact Number'))
    preferred_communication_method = models.CharField(max_length=20,choices= PreferredCommunicationChoices.choices,default=PreferredCommunicationChoices.EMAIL, verbose_name=_('Preferred Communication Method'))

    def __str__(self):
        return f"Profile for {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ["user__last_name"]
