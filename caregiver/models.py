from django.contrib.auth.models import User
from django.db import models


class Caregiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    first_name = models.CharField(max_length=15)
    surname = models.CharField(max_length=20)


class Shift(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
