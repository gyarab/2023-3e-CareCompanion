from django.contrib.auth.models import User
from django.db import models

from datetime import datetime


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='patient_profile')
    date_of_admission = models.DateField()
    room_number = models.IntegerField()
    birthday = models.DateField()
    health_info = models.TextField()

    objects = models.Manager()

    class ContactManager(models.Manager):
        def create_contact(self, patient, relationship, name, phone_number):
            return self.create(patient=patient, relationship=relationship, name=name, phone_number=phone_number)

    class MedicationIntakeManager(models.Manager):
        def create_medication(self, patient, medication, when, how):
            return self.create(patient=patient, medication=medication, when=when, how=how)

    medications = MedicationIntakeManager()
    contacts = ContactManager()
    fav_activities = models.CharField(max_length=255)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


class Contact(models.Model):
    RELATIONSHIP_CHOICES = (
        ('syn/dcera', 'Syn/Dcera'),
        ('pritel/kyne', 'Přítel/kyně'),
        ('sourozenec', 'Sourozenec'),
        ('rodic', 'Rodič'),
        ('manzel/ka', 'Manžel/ka'),
        ('jini pribuzni', 'Jiní příbuzní'),
        ('jine', 'Jiné'),
    )
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    name = models.CharField(max_length=25)
    phone_number = models.IntegerField(null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class MedicationIntake(models.Model):
    medication = models.CharField(max_length=50)

    WHEN_CHOICES = (
        ('rano', 'Ráno'),
        ('v poledne', 'V poledne'),
        ('vecer', 'Večer'),
        ('v noci', 'V noci'),
        ('jine', 'Jiné'),
    )
    when = models.CharField(max_length=20, choices=WHEN_CHOICES)

    HOW_CHOICES = (
        ('pred jidlem', 'Před jídlem'),
        ('s jídlem', 'S jídlem'),
        ('po jidle', 'Po jídle'),
        ('jine', 'Jiné'),
    )
    how = models.CharField(max_length=20, choices=HOW_CHOICES)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
