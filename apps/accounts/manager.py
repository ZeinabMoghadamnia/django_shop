from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager
class PhoneValidator(RegexValidator):
    regex = r'^(\+98|0)?9\d{9}$'
    message = "Phone number must be entered in the format: '+989199999933'."

class UserManager(models.Manager):
    def get_employees(self):
        return self.filter(discount_type='employee')

    def get_customers(self):
        return self.filter(discount_type='customer')