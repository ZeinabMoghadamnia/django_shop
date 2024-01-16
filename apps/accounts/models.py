from django.db import models
from django.utils.translation import gettext_lazy as _
from ..core.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
class User(AbstractUser, BaseModel):
    USER_TYPES = (
        ('costumer', 'Costumer'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, verbose_name=_('user type'),null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('email address'))
    mobile_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$', message=_("Please enter the phone number in this format: '09999999999'"))
    phone_number = models.CharField(validators=[mobile_regex], max_length=11, unique=True, verbose_name=_('phone'))
    first_name = models.CharField(max_length=40, verbose_name=_('first name'))
    last_name = models.CharField(max_length=40, verbose_name=_('last name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    image = models.ImageField(upload_to='users_profile_pics/', null=True, blank=True, verbose_name=_('image'))

    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'email']
    class Meta:
        verbose_name_plural = _('user')
    def __str__(self):
        return self.email


class Address(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('customer'))
    city = models.CharField(max_length=30, verbose_name=_('city'))
    province = models.CharField(max_length=30, verbose_name=_('province'))
    complete_address = models.TextField(max_length=200, verbose_name=_('complete address'))
    class Meta:
        verbose_name_plural = _('address')
    def __str__(self):
        return self.city
