from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from . import tasks


@receiver(post_save, sender=models.User)
def save_user(sender, instance, created, **kwargs):

    if created:
        if instance.type != 1:
            print('post_save user completed')
            print('send mail to', instance.email)

            from django.conf import settings
            from project.common import utils
            reminder = utils.random_with_N(10)
            instance.reminder = reminder
            instance.save()

            link = '{}/activate-email/{}'.format(
                settings.URL_WEBSITE,
                reminder
            )
            subject = 'Confirmación de cuenta de correo'
            utils.send_mail(
                recipient=[instance.email],
                subject=subject,
                template='email/welcome-app.html',
                context={
                        'display_name': instance.display_name(),
                        'site': settings.APPNAME,
                        'link': link
                }
            )
