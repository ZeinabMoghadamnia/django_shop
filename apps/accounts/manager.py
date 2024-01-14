from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager
class PhoneValidator(RegexValidator):
    regex = r'^(\+98|0)?9\d{9}$'
    message = "Phone number must be entered in the format: '+989199999933'."

class CostumeUserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, password):

        if not phone_number:
            raise ValueError("Entering a phone number is required!")
        if not email:
            raise ValueError("Entering a email address is required!")
        if not first_name:
            raise ValueError("Entering the first name is required!")
        if not last_name:
            raise ValueError("Entering the last name is required!")

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, password):

        user = self.create_user(phone_number, email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user