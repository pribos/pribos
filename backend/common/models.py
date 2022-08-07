import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedUUIDModel(models.Model):
	pkid = models.BigAutoField(primary_key=True, editable=False, verbose_name=_("pkid"))
	id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("id"))
	created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
	updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))

	class Meta:
		abstract = True
		ordering = ["-created", "-updated"]
	