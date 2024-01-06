from django.db import models


class Caretaker(models.Model):
    first_name = models.CharField(max_length=15)
    surname = models.CharField(max_length=20)


class Shift(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE)
