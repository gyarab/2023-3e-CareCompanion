from django.contrib.auth.models import User
from django.db import models


# Patient model
class Patient(models.Model):
    # Vztah jeden-na-jednoho s modelem User
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='patient_profile')
    room_number = models.IntegerField()
    birthday = models.DateField()
    health_info = models.TextField()
    observations = models.TextField(blank=True, null=True)

    # Pomáha spravovat objekty (v tomto případě contacts, medications, activities)
    objects = models.Manager()

    class ContactManager(models.Manager):
        # Funkce pro vytvoření konktaktu
        def create_contact(self, patient, relationship, name, phone_number):
            return self.create(patient=patient, relationship=relationship, name=name, phone_number=phone_number)

    class MedicationIntakeManager(models.Manager):
        # Funkce pro vytvoření medikace
        def create_medication(self, patient, medication, when, how):
            return self.create(patient=patient, medication=medication, when=when, how=how)

    class ActivityManager(models.Manager):
        # Funkce pro vytvoření rozvrhu
        def create_activity(self, patient, date, time, description):
            return self.create(patient=patient, date=date, time=time, description=description)

    # Pro manipulaci s objekty MedicationIntake
    medications = MedicationIntakeManager()
    # Pro manipulaci s objekty Contact
    contacts = ContactManager()
    # Pro manipulaci s objekty Activity
    activities = ActivityManager()

    # Z přiřazeného modelu User si klient převezme křestní jméno a příjmení
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


# Contact model
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
    # Model phone_number je CharField z důvodu hezčího zobrazení na frontendu
    phone_number = models.CharField(null=True, max_length=15)
    # Asociace kontaktu s klientem
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


# MedicationIntake model
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
        ('pred jidlem', 'před jídlem'),
        ('s jidlem', 's jídlem'),
        ('po jidle', 'po jídle'),
        ('jine', 'jiné'),
    )
    how = models.CharField(max_length=20, choices=HOW_CHOICES)
    # Asociace medikace s klientem
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Activity(models.Model):
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    description = models.CharField(max_length=50)
    # Asociace rozvrhu s klientem
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
