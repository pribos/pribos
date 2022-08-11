from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from common.models import TimeStampedUUIDModel
from djmoney.money import Money
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
User = settings.AUTH_USER_MODEL


class Tag(TimeStampedUUIDModel):
    name = models.CharField(max_length=200, verbose_name=_("name"))

    def __str__(self):
        return self.name


# status 선택지
class StatusType(models.TextChoices):
    NotStarted = "Not Started"
    InProgress = "In Progress"
    Done = "Done"


class Task(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("title"))
    country = CountryField(blank_label="(select country)", default='KR', null=True, blank=True, verbose_name=_("country"))  # ex) NZ / country.name -> New Zealand / country.flag
    income = MoneyField(
        max_digits=14, decimal_places=2,
        default_currency="KRW", null=True,
        verbose_name=_("income"))
    expected_pay_day = models.DateTimeField(null=True, blank=True, verbose_name=_("expected_pay_day"))
    actual_pay_day = models.DateTimeField(null=True, blank=True, verbose_name=_("actual_pay_day"))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_("deadline"))
    submit_day = models.DateTimeField(null=True, blank=True, verbose_name=_("submit_day"))
    client = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("client"))
    agency = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("agency"))
    status = models.CharField(
        max_length=15,
        choices=StatusType.choices,
        default=StatusType.NotStarted,
        verbose_name=_("status")
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("tags"))
    visible = models.BooleanField(max_length=1, default=True, verbose_name=_("visible"))

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-created', '-updated']

    @property
    def list_of_tags(self):
        tags = [tag.name for tag in self.tags.all()]
        return tags
