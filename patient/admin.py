from django.contrib import admin
from .models import Patient, Contact, MedicationIntake


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class MedicationIntakeInline(admin.TabularInline):
    model = MedicationIntake
    extra = 0


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'room_number')
    inlines = [ContactInline, MedicationIntakeInline]


admin.site.register(Patient, PatientAdmin)
