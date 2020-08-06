# from allauth.utils import build_absolute_uri
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import FieldDoesNotExist
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.encoding import force_text
from django.utils.six.moves.urllib.parse import urlsplit
from django.conf import settings
from . import models
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_user_by_code(code=''):
    qs = models.User.objects.filter(reminder=code)
    return qs.first()


def user_by_email(email='', role=None):
    qs = models.User.objects.filter(email=email)
    if role:
        qs = qs.filter(role__in=role)

    return qs.first()


def user_by_username(username, role=None):
    qs = models.User.objects.filter(username=username)
    if role:
        qs = qs.filter(role__in=role)

    return qs.first()


def user_field(user, field, *args):
    """
    Gets or sets (optional) user model fields. No-op if fields do not exist.
    """
    if not field:
        return
    User = get_user_model()
    try:
        field_meta = User._meta.get_field(field)
        max_length = field_meta.max_length
    except FieldDoesNotExist:
        if not hasattr(user, field):
            return
        max_length = None
    if args:
        # Setter
        v = args[0]
        if v:
            v = v[0:max_length]
        setattr(user, field, v)
    else:
        # Getter
        return getattr(user, field)


def user_username(user, *args):
    # if args and not app_settings.PRESERVE_USERNAME_CASING and args[0]:
    if args and not True and args[0]:
        args = [args[0].lower()]
    return user_field(user, 'username', *args)


def user_email(user, *args):
    return user_field(user, 'email', *args)


def build_absolute_uri(request, location, protocol=None):
    """request.build_absolute_uri() helper

    Like request.build_absolute_uri, but gracefully handling
    the case where request is None.
    """
    # from .account import app_settings as account_settings

    if request is None:
        site = Site.objects.get_current()
        bits = urlsplit(location)
        if not (bits.scheme and bits.netloc):
            uri = '{proto}://{domain}{url}'.format(
                proto='http',
                domain=site.domain,
                url=location)
        else:
            uri = location
    else:
        uri = request.build_absolute_uri(location)
    # NOTE: We only force a protocol if we are instructed to do so
    # (via the `protocol` parameter, or, if the default is set to
    # HTTPS. The latter keeps compatibility with the debatable use
    # case of running your site under both HTTP and HTTPS, where one
    # would want to make sure HTTPS links end up in password reset
    # mails even while they were initiated on an HTTP password reset
    # form.
    # if not protocol and account_settings.DEFAULT_HTTP_PROTOCOL == 'https':
        # protocol = account_settings.DEFAULT_HTTP_PROTOCOL
    if not protocol:
        protocol = 'http'
    # (end NOTE)
    if protocol:
        uri = protocol + ':' + uri.partition(':')[2]
    return uri


def format_email_subject(subject, request):
    prefix = None
    if prefix is None:
        site = get_current_site(request)
        prefix = "[{name}] ".format(name=site.name)
    return prefix + force_text(subject)


def get_email_confirmation_url(request, user):
    """Constructs the email confirmation (activation) url.

    Note that if you have architected your system such that email
    confirmations are sent outside of the request context `request`
    can be `None` here.
    """
    url = reverse(
        "security:account_confirm_email",
        args=[user.key])
    ret = build_absolute_uri(
        request,
        url)
    return ret


def get_from_email():
    """
    This is a hook that can be overridden to programatically
    set the 'from' email address for sending emails
    """
    return settings.DEFAULT_FROM_EMAIL


def render_mail(template_prefix, email, context, request):
    """
    Renders an e-mail to `email`.  `template_prefix` identifies the
    e-mail that is to be sent, e.g. "account/email/email_confirmation"
    """
    subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                               context)
    # remove superfluous line breaks
    subject = " ".join(subject.splitlines()).strip()
    subject = format_email_subject(subject, request)

    from_email = get_from_email()

    bodies = {}
    for ext in ['html', 'txt']:
        try:
            template_name = '{0}_message.{1}'.format(template_prefix, ext)
            bodies[ext] = render_to_string(template_name,
                                           context).strip()
        except TemplateDoesNotExist:
            if ext == 'txt' and not bodies:
                # We need at least one body
                raise
    if 'txt' in bodies:
        msg = EmailMultiAlternatives(subject,
                                     bodies['txt'],
                                     from_email,
                                     [email])
        if 'html' in bodies:
            msg.attach_alternative(bodies['html'], 'text/html')
    else:
        msg = EmailMessage(subject,
                           bodies['html'],
                           from_email,
                           [email])
        msg.content_subtype = 'html'  # Main content is now text/html
    return msg


def send_mail(template_prefix, email, context, request):
    msg = render_mail(template_prefix, email, context, request)
    msg.send()
