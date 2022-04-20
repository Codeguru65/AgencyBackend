from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

import config


class UserManager(BaseUserManager):

    def create_user(self, username, email, password,**extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None,**extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password,**extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

industry = (
    ('Consulting', 'Consulting'),
    ('Electronic Payments', 'Electronic Payments'),
    ('Banking', 'Banking'),
    ('Funeral Services', 'Funeral Services'),
    ('Micro Finance', 'Micro Finance'),
    ('Tertiary', 'Tertiary'),
    ('Clothing', 'Clothing'),
)


class Institution(models.Model):
    agent_check = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    client_address = models.CharField(max_length=500, blank=True)
    agent_category = models.ForeignKey('config.AgencyPricing', on_delete=models.CASCADE)
    mobile_1 = models.CharField(max_length=30, blank=True)
    mobile_2 = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=255)
    industry = models.CharField(max_length=255, choices=industry)
    street_name = models.CharField(max_length=255, blank=True)
    approved_logo = models.ImageField(upload_to='logos', blank=True)
    approved_colors = models.CharField(max_length=30, help_text='Upload Hex Colors Only', blank=True)

    class Meta:
        verbose_name = 'Institutional Agents'
        verbose_name_plural = 'Institutional Agents'

    @property
    def aml(self):
        return self.user_set.all()

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    mobile_number = models.CharField(max_length=255, unique=True, db_index=True)
    id_number = models.CharField(max_length=255, unique=True, db_index=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    password_reset_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','mobile_number','id_number' ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
