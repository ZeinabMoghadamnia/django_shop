from django.contrib import admin
from .models import User, Address, OtpCode

# Register your models here.

admin.site.register([User, Address, OtpCode])