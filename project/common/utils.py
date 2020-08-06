from django.conf import settings


def random_with_N(n):
    from random import randint
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_mail(recipient=[], subject='', template='', context={}, cc=[]):

    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string

    from_ = settings.DEFAULT_FROM_EMAIL
    bodythml = render_to_string(template, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=bodythml,
        from_email="{0} <{1}>".format(settings.APPNAME, from_),
        to=recipient,
        cc=cc
    )
    email.attach_alternative(bodythml, "text/html")
    return email.send()
