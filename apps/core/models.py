from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import BaseManager
from django.utils import timezone

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('date created'))
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('date updated'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('delete status'))
    deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('date deleted'))
    restored_at = models.DateTimeField(auto_now=True, blank=True, null=True , verbose_name=_('date restored'))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    # expired_at = models.DateTimeField(null=True, blank=True, verbose_name=_('expired'))
    objects = BaseManager()
    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

