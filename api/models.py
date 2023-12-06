from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Users(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField( max_length=50, null=False,unique=True,blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    password = models.CharField(max_length=50, null=False)
    is_staff = models.BooleanField(default=False)

    objects = Users()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


    