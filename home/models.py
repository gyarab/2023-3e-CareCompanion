from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)


class Address(models.Model):
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)


class DaySchedule(models.Model):
    time = models.TimeField()
    description = models.CharField(max_length=50)


class Announcement(models.Model):
    text = models.TextField()
    delete_when = models.DateTimeField()
