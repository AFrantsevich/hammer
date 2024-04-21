from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    personal_referral_code = models.CharField(max_length=6,
                                              blank=True, null=True,
                                              unique=True, default=None)

    referral_code = models.ForeignKey('CustomUser',
                                      on_delete=models.CASCADE,
                                      related_name='my_referral_users',
                                      null=True, default=None)

    def __str__(self):
        return self.phone
