from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email               = self.normalize_email(email),
            username            = username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(
            email               = email,
            password            = password,
            username            = username,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username            = models.CharField(max_length=255, unique=True)
    email               = models.EmailField(
        verbose_name  = 'email address',
        max_length    = 255,
        unique        = True,
    )
    
    profile_image       = models.ImageField(null=True, blank=True, upload_to='users/')
    favourite_fruites   = models.ManyToManyField('shop.Product', blank=True)
    is_active           = models.BooleanField(default=True)
    is_admin            = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin