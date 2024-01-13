from django.db import models
from ..core.models import BaseModel
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
# Create your models here.

# class Member(AbstractUser, BaseModel):
#     phone = models.CharField(max_length=11, unique=True)

class CustomUserManager(BaseUserManager, BaseModel):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class Member(AbstractUser, BaseModel):
    CUSTOMERUSER_EMPLOYEE = 'e'
    CUSTOMERUSER_CUSTOMER = 'c'
    CUSTOMERUSER_MANAGER = 'm'
    CUSTOMERUSER_STATUS = (
        (CUSTOMERUSER_EMPLOYEE,'employee'),
        (CUSTOMERUSER_CUSTOMER,'customer'),
        (CUSTOMERUSER_MANAGER,'manager')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    birth_day = models.DateField(null=True, blank=True)
    mobile_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$', message="Phone number must be entered in the format: '+989199999933'.")
    phone_number = models.CharField(validators=[mobile_regex], max_length=20, unique=True)
    user_type = models.CharField(max_length=1,choices=CUSTOMERUSER_STATUS, default=CUSTOMERUSER_CUSTOMER)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='covers/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    user_create = CustomUserManager()

    objects = CustomUserManager()

