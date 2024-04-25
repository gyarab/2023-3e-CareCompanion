from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django import forms

from caregiver.models import Shift
from patient.models import Patient, Contact as Patient_contact, MedicationIntake, Activity


# Vytvoření všech formulářů, které se v projektu používají

# Univerzální formulář pro ModelForm, která bootstrapuje všechny jeho fields
class DefaultBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


# Formulář pro registraci uživatelského účtu
class RegisterUserForm(UserCreationForm):
    GROUP_CHOICES = (
        ('Patients', 'Klient'),
        ('Admins', 'Admin'),
        ('Caregivers', 'Opatrovník'),
    )

    groups = forms.ChoiceField(
        choices=GROUP_CHOICES,
        widget=forms.Select,
        required=True,
        label='Typ uživatele',
    )

    first_name = forms.CharField(max_length=30, required=True, label='Křestní jméno')
    last_name = forms.CharField(max_length=30, required=True, label='Příjmení')

    class Meta:
        model = User
        fields = ('groups', 'first_name', 'last_name', 'username', 'password1', 'password2')
        labels = {
            'username': 'Uživatelské jméno',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        group_name = self.cleaned_data.get('groups')
        # Z vyplňeného formuláře získáme skupinu (typ) uživatele, který byl vytvořen
        group = Group.objects.get(name=group_name)
        # Zadané username převedeme na malá písmena
        username_lower = self.cleaned_data.get('username').lower()
        user.username = username_lower

        if commit:
            user.save()
            user.groups.set([group])
        return user

    # Nevyužijeme 'DefaultBootstrapForm', protože tato forma není třídy 'forms.ModelForm'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


# Formulář pro úpravu informací již vytvořených uživatelských účtů
class UpdateUsersInformationForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=30, required=True, label='Křestní jméno')
    last_name = forms.CharField(max_length=30, required=True, label='Příjmení')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'username': 'Uživatelské jméno'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


# Formulář pro resetování hesla
class ResetUserPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


# Formulář pro vytvoření klienta - modelu Patient
class PatientForm(DefaultBootstrapForm):
    user = forms.ModelChoiceField(
        # Nabízení uživatelé jsou ti, kteří mají skupinu 'Patients' a ještě nemají přiřazený vlastní model Patient
        queryset=User.objects.filter(groups__name='Patients').exclude(patient_profile__isnull=False),
        widget=forms.Select,
        required=True,
        label='Uživatel'
    )

    class Meta:
        model = Patient
        fields = ['user', 'room_number', 'birthday', 'health_info', 'observations']
        widgets = {
            'user': forms.Select(),
            'date_of_admission': forms.DateInput(attrs={'type': 'date'}),
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'room_number': 'Číslo pokoje',
            'birthday': 'Datum narození',
            'health_info': 'Informace o zdraví',
            'observations': 'Postřehy'
        }
        help_texts = {
            'observations': 'Postřehy opatrovníku nebo informace ke klientovi poskytnuté blízkými nebo jím samotným',
        }


# Formulář pro klientské kontakty
class PatientContactForm(DefaultBootstrapForm):
    class Meta:
        model = Patient_contact
        fields = ['relationship', 'name', 'phone_number']
        labels = {
            'relationship': 'Vztah',
            'name': 'Jméno',
            'phone_number': 'Telefonní číslo'
        }


# Formulář pro klientskou medikaci
class MedicationIntakeForm(DefaultBootstrapForm):
    class Meta:
        model = MedicationIntake
        fields = ['medication', 'when', 'how']
        labels = {
            'medication': 'Lék',
            'when': 'Kdy',
            'how': 'Jak'
        }


# Formulář pro úpravu existujících klientů
class UpdatePatientForm(DefaultBootstrapForm):
    class Meta:
        model = Patient
        fields = ['room_number', 'birthday', 'health_info', 'observations']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'date_of_admission': 'Datum přijetí',
            'room_number': 'Číslo pokoje',
            'birthday': 'Datum narození',
            'health_info': 'Informace o zdraví',
            'observations': 'Postřehy'
        }
        help_texts = {
            'observations': 'Postřehy opatrovníku nebo informace ke klientovi poskytnuté blízkými nebo jím samotným',
        }


# Formulář pro postřehy o klientovi
class ObservationForm(DefaultBootstrapForm):
    class Meta:
        model = Patient
        fields = ['observations']
        labels = {
            'observations': ''
        }
        help_texts = {
            'observations': 'Jakákoliv vypozorovaná zajímavá fakta ke klientovi (např. zájmy, oblíbená témata, aktivity..)'
        }


# Formulář pro klientské rozvrhy
class PatientActivityForm(DefaultBootstrapForm):
    class Meta:
        model = Activity
        fields = ['date', 'time', 'description']
        labels = {
            'date': 'Datum',
            'time': 'Čas',
            'description': 'Popis'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }


# Formulář pro směny opatrovníků
class CaregiverShiftForm(DefaultBootstrapForm):
    class Meta:
        model = Shift
        fields = ['date_of_shift', 'start', 'end']
        labels = {
            'date_of_shift': 'Datum',
            'start': 'Začátek',
            'end': 'Konec'
        }
        widgets = {
            'date_of_shift': forms.DateInput(attrs={'type': 'date'}),
            'start': forms.TimeInput(attrs={'type': 'time'}),
            'end': forms.TimeInput(attrs={'type': 'time'}),
        }
