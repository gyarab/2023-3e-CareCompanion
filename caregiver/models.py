from django.contrib.auth.models import User
from django.db import models


# Caregiver model
class Caregiver(models.Model):
    # Vztah jeden-na-jednoho s modelem User
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='caregiver_profile')
    # Pomáha spravovat objekty (v tomto případě shifts)
    objects = models.Manager()

    class ShiftManager(models.Manager):
        # Funkce pro vytvoření směny
        def create_shift(self, caregiver, date_of_shift, start, end):
            return self.create(caregiver=caregiver, date_of_shift=date_of_shift, start=start, end=end)

    # Pro manipulaci s objekty Shift
    shifts = ShiftManager()

    # Z přiřazeného modelu User si opatrovník převezme křestní jméno a příjmení
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


# Shift model
class Shift(models.Model):
    date_of_shift = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    # Boolean funkce vracící jestli je směna přes noc - tato fce je využita ve views.py u opat. i klienta
    def is_overnight_shift(self):
        if self.end < self.start:
            return True
        return False

    # Asociace směny s opatrovníkem
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
