import os
from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class FieldDefaultsAbstracts(models.Model):
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )
    disabled_at = models.DateTimeField(
        _('Disabled at'),
        auto_now=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True
    )

    class Meta:
        abstract = True