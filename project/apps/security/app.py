from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserConfig(AppConfig):
    name = 'project.apps.security'
    verbose_name = _('security')

    def ready(self):
        import project.apps.security.signals
