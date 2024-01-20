from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='patient_profile')
    first_name = models.CharField(max_length=15)
    surname = models.CharField(max_length=20)
    birthday = models.DateField()
    room_number = models.IntegerField()
    health_info = models.CharField(max_length=255)
    fav_activities = models.TextField()

    class ContactManager(models.Manager):
        def create_contacts(self, contacts):
            for contact_data in contacts:
                self.create(**contact_data)

    class MedicationIntakeManager(models.Manager):
        def create_medications(self, medications):
            for medication_data in medications:
                self.create(**medication_data)

    objects = models.Manager()
    contacts = ContactManager()
    medications = MedicationIntakeManager()


class Contact(models.Model):

    RELATIONSHIP_CHOICES = (
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
