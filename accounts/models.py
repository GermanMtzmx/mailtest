from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import models

from django.core.validators import (
    FileExtensionValidator, RegexValidator)

from common.models import BaseModel
from common import regex

from .utils import (
    generate_user_renewed,
    generate_code, generate_code_expired)


class User(BaseModel):
    """User model"""

    firstName = models.CharField(max_length=150, null=False, blank=False)
    lastName = models.CharField(max_length=150, null=False, blank=False)

    username = models.CharField(max_length=200,
        unique=True, null=False, blank=False,
        validators=[RegexValidator(regex.USERNAME)])
    password = models.CharField(max_length=106, null=False, blank=False)

    email = models.EmailField(null=False, blank=False)
    birthday = models.DateField(null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)

    avatar = models.ImageField(null=True, blank=True,
        upload_to='files/avatars/d%Y%m%d/',
        validators=[FileExtensionValidator(['png', 'jpg'])])

    renewed = models.BigIntegerField(default=generate_user_renewed, null=True, blank=True)
    isActive = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = make_password(password)
        self.renewed = generate_user_renewed()
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('username',)


class SignUpCode(BaseModel):
    """Sign up code model"""

    email = models.EmailField(null=False, blank=False)
    code = models.CharField(max_length=4, null=False,
        blank=False, editable=False, default=generate_code)

    expired = models.DateTimeField(editable=False, default=generate_code_expired)
    created = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.expired

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'accounts_sign_up_code'
        verbose_name = _('sign up code')
        verbose_name_plural = _('sign up codes')
        ordering = ('email',)


class SocialToken(BaseModel):
    """Social token model"""

    SOCIALS = (
        ('facebook', _('Facebook')),
        ('twitter', _('Twitter'))
    )

    social = models.CharField(max_length=10, null=False, blank=False, choices=SOCIALS)

    token = models.CharField(max_length=120, null=False, blank=False, unique=True)

    user = models.OneToOneField('accounts.User',
        on_delete=models.CASCADE, null=False,
        blank=False, db_column='user')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'accounts_social_token'
        verbose_name = _('social token')
        verbose_name_plural = _('social tokens')
        ordering = ('token',)

