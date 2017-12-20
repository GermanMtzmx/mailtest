from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.core.validators import (
    FileExtensionValidator, RegexValidator)

from rest_framework import serializers

from common.utils import get_object_or_none, to_object
from common import regex

from .auth import authenticate, auth_token, passwd_token
from .models import User, SignUpCode, SocialToken
from .tasks import send_signup_mail, send_passwd_reset_mail
from django.core.mail import EmailMessage



class SignUpExistsSerializer(serializers.Serializer):
    """Sign up exists serializer"""

    username = serializers.CharField(max_length=200)

    def validate_username(self, value):
        user = get_object_or_none(User, username=value)
        if not user:
            raise serializers.ValidationError(
                _('User does not exist.'))
        return value

    def create(self, validated_data):
        return to_object(validated_data)


class SignUpMailSerializer(serializers.ModelSerializer):
    """Sign up mail serializer"""

    def validate_email(self, value):
        codes = User.objects.filter(email=value)
        if codes.count() > settings.SIGNUP_EMAIL_USE_LIMIT:
            raise serializers.ValidationError(
                _('This email address '
                    'has been used many times.'))
        return value

    def create(self, validated_data):
        SignUpCode.objects.filter(Q(
            Q(email=validated_data['email']) |
            Q(expired__lt=timezone.now())
        )).delete() # Delete sign up codes

        instance = super(self.__class__,
            self).create(validated_data)

        send_signup_mail.delay(
            instance.code, instance.email)
        return instance

    class Meta:
        model = SignUpCode
        exclude = ('code', 'expired')


class SignUpCheckSerializer(serializers.Serializer):
    """Sign up check serializer"""

    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        obj = get_object_or_none(SignUpCode,
            email=attrs['email'], code=attrs['code'])
        if not obj:
            SignUpCode.objects.filter(
                email=attrs['email']
            ).delete() # Delete sign up codes
            raise serializers.ValidationError({
                'code': _('Invalid code.')})

        if not obj.is_valid():
            obj.delete() # Delete sign up code
            raise serializers.ValidationError({
                'code': _('Invalid code.')})
        return attrs

    def create(self, validated_data):
        return to_object(validated_data)


class SignUpSerializer(serializers.ModelSerializer):
    """Sign up serializer"""

    password = serializers.CharField(max_length=200,
        validators=[RegexValidator(regex.PASSWORD)])

    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        obj = get_object_or_none(SignUpCode,
            email=attrs['email'], code=attrs['code'])
        if not obj:
            raise serializers.ValidationError({
                'code': _('Invalid code.')})

        if not obj.is_valid():
            obj.delete() # Delete sign up code
            raise serializers.ValidationError({
                'code': _('Invalid code.')})

        self.context['code'] = obj
        return attrs

    def create(self, validated_data):
        self.context['code'].delete() # Delete sign up code
        validated_data.pop('code')

        instance = super(self.__class__, self).create(validated_data)
        instance.set_password(validated_data['password'])
        return instance

    class Meta:
        model = User
        exclude = ('avatar', 'isActive', 'renewed')


class SocialSignUpSerializer(serializers.ModelSerializer):
    """Social sign up serializer"""

    social = serializers.CharField(max_length=10)
    token = serializers.CharField(max_length=120)

    def validate_social(self, value):
        socials = ('facebook', 'twitter')
        if not value in socials:
            raise serializers.ValidationError(
                _('Social does not exist.'))
        return value

    def validate_token(self, value):
        token = get_object_or_none(SocialToken, token=value)
        if token:
            raise serializers.ValidationError(
                _('Token already in use.'))
        return value

    def create(self, validated_data):
        validated_data['password'] = validated_data['token']

        social = validated_data.pop('social')
        token = validated_data.pop('token')

        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])

        SocialToken.objects.create(
            user=user, social=social, token=token)
        return user

    class Meta:
        model = User
        exclude = ('avatar',
            'isActive', 'renewed', 'password')


class SignInSerializer(serializers.Serializer):
    """Sign in serializer"""

    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate_username(self, value):
        user = get_object_or_none(User, username=value)
        if not user:
            raise serializers.ValidationError(
                _('User does not exist.'))

        if not user.isActive:
            raise serializers.ValidationError(
                _('User inactive.'))

        self.context['user'] = user
        return value

    def validate(self, attrs):
        user = authenticate(attrs['username'],
            attrs['password'], instance=self.context['user'])
        if not user:
            raise serializers.ValidationError({
                'password': _('Incorrect password.')})
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        user.token = auth_token(user)
        return user


class SocialSignInSerializer(serializers.Serializer):
    """Social sign in serializer"""

    social = serializers.CharField(max_length=10)

    username = serializers.CharField(max_length=200)
    token = serializers.CharField(max_length=120)

    def validate_social(self, value):
        socials = ('facebook', 'twitter')
        if not value in socials:
            raise serializers.ValidationError(
                _('Social does not exist.'))
        return value

    def validate_username(self, value):
        token = get_object_or_none(
            SocialToken, user__username=value)
        if not token:
            raise serializers.ValidationError(
                _('There is no social '
                    'token with this username.'))

        if not token.user.isActive:
            raise serializers.ValidationError(
                _('User inactive.'))

        self.context['token'] = token
        return value

    def validate(self, attrs):
        token = self.context['token']
        if token.social != attrs['social']\
            or token.token != attrs['token']:
            token = None

        if not token:
            raise serializers.ValidationError({
                'token': _('Incorrect token.')})
        return attrs

    def create(self, validated_data):
        user = self.context['token'].user
        user.token = auth_token(user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""

    class Meta:
        model = User
        exclude = ('password', 'isActive', 'renewed')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Profile update serializer"""

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'birthday')


class AvatarSerializer(serializers.ModelSerializer):
    """Avatar serializer"""

    def validate_avatar(self, value):
        if value.size > 1048576:
            raise serializers.ValidationError(
                _('The maximum file size is 1 MB.'))
        return value

    class Meta:
        model = User
        fields = ('avatar',)
        extra_kwargs = {'avatar': {'required': True}}


class ChangeSerializer(serializers.Serializer):
    """Password change serializer"""

    old = serializers.CharField(max_length=200)
    new = serializers.CharField(max_length=200,
        validators=[RegexValidator(regex.PASSWORD)])

    def validate_old(self, value):
        if not authenticate(self.instance.username,
            value, instance=self.instance):
            raise serializers.ValidationError(
                _('Incorrect password.'))
        return value

    def validate(self, attrs):
        if attrs['old'] == attrs['new']:
            raise serializers.ValidationError(
                _('New and old password cannot be same.'))
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new'])
        return instance


class ResetMailSerializer(serializers.Serializer):
    """Password reset mail serializer"""

    username = serializers.CharField(max_length=200)

    def validate_username(self, value):
        user = get_object_or_none(User, username=value)
        if not user:
            raise serializers.ValidationError(
                _('User does not exist.'))

        self.context['user'] = user
        return value

    def create(self, validated_data):
        user = self.context['user']
        token = passwd_token(user)

        send_passwd_reset_mail.delay(
            token, user.username, user.email)
        return user


class ResetSerializer(serializers.Serializer):
    """Password reset serializer"""

    password = serializers.CharField(max_length=200,
        validators=[RegexValidator(regex.PASSWORD)])

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        return instance
