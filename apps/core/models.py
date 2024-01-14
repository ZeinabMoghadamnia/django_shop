from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('date created'))
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('date updated'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('delete status'))
    deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('date deleted'))
    restored_at = models.DateTimeField(auto_now=True, blank=True, null=True , verbose_name=_('date restored'))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    class Meta:
        abstract = True
