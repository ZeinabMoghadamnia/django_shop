from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
# from social_core.backends import username

from ..core.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission


# from .managers import MyUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    phone_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$', message="Phone number must be entered in the format: '+989199999933'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='users_profile_pics/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='user_accounts')
    user_permissions = models.ManyToManyField(Permission, related_name='user_accounts_permissions')

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name', 'email']

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
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    City = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    complete_address = models.TextField(max_length=200)
    # home_plate = models.CharField(max_length=20)
    # postal_code = models.CharField(max_length=20)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
