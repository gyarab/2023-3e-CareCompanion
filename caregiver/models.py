from django.contrib.auth.models import User
from django.db import models


class Caregiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='caregiver_profile')
    first_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)

    objects = models.Manager()

    class ShiftManager(models.Manager):
        def create_shift(self, caregiver, date, start, end):
            return self.create(caregiver=caregiver, date=date, start=start, end=end)

    shifts = ShiftManager()


class Shift(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    class ActivityManager(models.Manager):
        def create_activity(self, shift, time, description):
            return self.create(shift=shift, time=time, description=description)

    activities = ActivityManager()

    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)


class Activity(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    time = models.TimeField()
    description = models.CharField(max_length=255)
