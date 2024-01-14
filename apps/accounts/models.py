from django.db import models
from django.utils.translation import gettext_lazy as _
from ..core.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission
from .manager import PhoneValidator


class User(AbstractUser):
    USER_TYPES = (
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('customer', 'Customer'),
    )
    discount_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer', verbose_name=_('user type'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('email address'))
    phone_number = models.CharField(validators=[PhoneValidator], max_length=11, unique=True, verbose_name=_('phone'))
    first_name = models.CharField(max_length=40, verbose_name=_('first name'))
    last_name = models.CharField(max_length=40, verbose_name=_('last name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    image = models.ImageField(upload_to='users_profile_pics/', null=True, blank=True, verbose_name=_('image'))

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'email']
    def __str__(self):
        return self.email


class Address(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('customer'))
    city = models.CharField(max_length=30, verbose_name=_('city'))
    province = models.CharField(max_length=30, verbose_name=_('province'))
    complete_address = models.TextField(max_length=200, verbose_name=_('complete address'))
    def __str__(self):
        return self.city
