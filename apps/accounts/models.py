from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
# from social_core.backends import username

from ..core.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission


# from .managers import MyUserManager


class User(AbstractUser):
    USER_TYPES = (
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('customer', 'Customer'),
    )
    discount_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer', verbose_name=_('user type'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('email address'))
    phone_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$', message="Phone number must be entered in the format: '+989199999933'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True, verbose_name=_('phone'))
    first_name = models.CharField(max_length=40, verbose_name=_('first name'))
    last_name = models.CharField(max_length=40, verbose_name=_('last name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    image = models.ImageField(upload_to='users_profile_pics/', null=True, blank=True, verbose_name=_('image'))
    # groups = models.ManyToManyField(Group, related_name='user_accounts')
    # user_permissions = models.ManyToManyField(Permission, related_name='user_accounts_permissions')

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'email']

    # class Meta:
    #     verbose_name = _('User')
    #     verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    # def save(self, *args, **kwargs):
    #     self.username = self.email
    #     super().save(*args, **kwargs)


class Address(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('customer'))
    city = models.CharField(max_length=30, verbose_name=_('city'))
    province = models.CharField(max_length=30, verbose_name=_('province'))
    complete_address = models.TextField(max_length=200, verbose_name=_('complete address'))
    def __str__(self):
        return self.city
