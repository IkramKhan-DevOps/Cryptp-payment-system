from django.contrib.auth.models import AbstractUser
from django.db import models
from payapp.utils import convert_crypto


class User(AbstractUser):
    CURRENCY_TYPE = (
        ('BTC', 'BTC'),
        ("DOGE", 'DOGE'),
        ("ETHEREUM", 'ETHEREUM'),
    )

    email = models.EmailField(unique=True, max_length=200)
    total_amount = models.FloatField(default=10)
    sent_amount = models.FloatField(default=0)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default='BTC')

    REQUIRED_FIELDS = ['username', ]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    def get_name_info(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

