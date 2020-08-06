from django.conf import settings
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext as _
from .adapters import DefaultAccountAdapter
from . import utils

# JWTSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from . import models
User = get_user_model()


def get_adapter():
    return DefaultAccountAdapter()


class JWTLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name',)
        read_only_fields = ('email',)


class ResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={
        'input_type': 'password'
    })
    password_confirm = serializers.CharField(required=True, style={
        'input_type': 'password'
    })

    def validate_code(self, code):
        user = utils.get_user_by_code(code=code)

        if not user:
            msg = _('Not exist code')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )

        return data


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    type = serializers.ChoiceField(required=True, choices=User.USER_TYPE)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        # if allauth_settings.UNIQUE_EMAIL:
        if True:
            # if email and email_address_exists(email):
            if email and User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password_confirm')
        # user_type = data.get('type')
        if password1 != password2:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('email'),
            'password': self.validated_data.get('password_confirm', ''),
            'email': self.validated_data.get('email', ''),
            'type': self.validated_data.get('type', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password_confirm',
            'type',
        ]


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'photo',
            'type'
        ]
        read_only_fields = ('email', 'username', 'type', 'id')


class LoginAppSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    user_type = serializers.CharField(required=False, allow_blank=True)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        elif username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password"')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user_type = attrs.get('user_type', '2')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                UserModel = User
                try:
                    username = UserModel.objects.get(
                        email__iexact=email
                    ).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        # If context site is equals to user profile
        # current_domain = self.context.get('request').META.get('HTTP_REFERER')
        type_to_comparate = user_type
        # if current_domain in settings.REST_LOGIN_URLS.get('LADING'):
        #     type_to_comparate = 1
        # if current_domain in settings.REST_LOGIN_URLS.get('CLIENT'):
        #     type_to_comparate = 2

        if str(user.type) != type_to_comparate:
            raise serializers.ValidationError(_('Cuenta no válida'))

        attrs['user'] = user
        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['display_name'] = user.display_name()
        # print(token)
        # ...

        return token
