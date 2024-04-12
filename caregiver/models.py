from django.contrib.auth.models import User
from django.db import models


class Caregiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='caregiver_profile')
    objects = models.Manager()

    class ShiftManager(models.Manager):
        def create_shift(self, caregiver, date_of_shift, start, end):
            return self.create(caregiver=caregiver, date_of_shift=date_of_shift, start=start, end=end)

    shifts = ShiftManager()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


class Shift(models.Model):
    date_of_shift = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
