import os
import datetime

from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core import signing
from django.db import models


# Method rename files
def path_and_rename(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'users/{}/profile/'.format(obj.email)

    # return the whole path to the file
    return os.path.join(path, filename)


class User(AbstractUser):

    USER_TYPE = (
        (1, _("Administrador")),
        (2, _("Empresa")),
        (3, _("Staff")),
    )
    type = models.IntegerField(
        choices=USER_TYPE,
        verbose_name=_('Rol'),
        default=1
    )
    photo = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True,
        verbose_name=_('Foto de perfil')
    )
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    email_verified = models.BooleanField(
        verbose_name=_('Email verificado?'),
        default=False
    )
    reminder = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'type', 'first_name', 'last_name']

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)

    @property
    def key(self):
        return signing.dumps(
            obj=self.pk,
            salt=settings.SECRET_KEY
        )

    @classmethod
    def from_key(cls, key):
        try:
            max_age = (
                # 60 * 60 * 24 * app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS)
                60 * 60 * 24 * 1)
            pk = signing.loads(
                key,
                max_age=max_age,
                # salt=app_settings.SALT)
                salt=settings.SECRET_KEY)
            ret = User.objects.get(pk=pk)
        except (signing.SignatureExpired,
                signing.BadSignature,
                User.DoesNotExist):
            ret = None
        return ret

    def display_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return '{} {}'.format(self.first_name, self.last_name)

    def key_expired(self):
        days = 1
        expiration_date = self.created + datetime.timedelta(days=days)
        return expiration_date <= timezone.now()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
