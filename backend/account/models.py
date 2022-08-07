from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = None
    email = models.EmailField(verbose_name=_('email address'), unique=True, db_index=True)
    name = models.CharField(verbose_name=_("first name"), max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created = models.DateTimeField(default=timezone.now)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = (_("user"))
        verbose_name_plural = (_("users"))

    def __str__(self):
        return self.name