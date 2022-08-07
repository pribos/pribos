from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("You must provide a valid email address"))



    def _create_user(self, email, password, name, **extra_fields):
        """Create a user with the given email and password."""

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        else:
            raise ValidationError(_("Admin Account: An email address is required"))

        if not name:
            raise ValueError(_("Users must submit a name"))

        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_user(self, email, password, name, **extra_fields):
        """Create and save a regular user with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, name, **extra_fields)


        

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))

        if not password:
            raise ValueError(_("Superusers must have a password"))
        
        return self._create_user(email, password, name, **extra_fields)
  