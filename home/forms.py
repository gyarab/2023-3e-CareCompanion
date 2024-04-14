from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django import forms

from patient.models import Patient, Contact as Patient_contact, MedicationIntake
from .models import Contact as Institute_contact, Address, DaySchedule, Announcement


class RegisterUserForm(UserCreationForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select,
        required=True,
        label='Typ uživatele'
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
        group = self.cleaned_data.get('groups')

        if commit:
            user.save()
            user.groups.set([group])
        return user

    # Bootstrap
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Patients').exclude(patient_profile__isnull=False),
        widget=forms.Select,
        required=True,
        label='Uživatel'
    )

    class Meta:
        model = Patient
        fields = ['user', 'date_of_admission', 'room_number', 'birthday', 'health_info', 'observations']
        widgets = {
            'user': forms.Select(),
            'date_of_admission': DateInput(),
            'birthday': DateInput()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'form-control'
        self.fields['user'].widget.attrs['label'] = 'Uzivatel'
        self.fields['date_of_admission'].widget.attrs['class'] = 'form-control'
        self.fields['room_number'].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control'
        self.fields['health_info'].widget.attrs['class'] = 'form-control'
        self.fields['observations'].widget.attrs['class'] = 'form-control'


class PatientContactForm(forms.ModelForm):
    class Meta:
        model = Patient_contact
        fields = ['relationship', 'name', 'phone_number']
        labels = {
            'relationship': 'Vztah',
            'name': 'Jméno',
            'phone number': 'Telefonní číslo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['relationship'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'


class MedicationIntakeForm(forms.ModelForm):
    class Meta:
        model = MedicationIntake
        fields = ['medication', 'when', 'how']
        labels = {
            'medication': 'Lék',
            'when': 'Kdy',
            'how': 'Jak'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medication'].widget.attrs['class'] = 'form-control'
        self.fields['when'].widget.attrs['class'] = 'form-control'
        self.fields['how'].widget.attrs['class'] = 'form-control'


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
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'


class ResetUserPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_admission', 'room_number', 'birthday', 'health_info', 'observations']
        widgets = {
            'date_of_admission': DateInput(),
            'birthday': DateInput()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_admission'].widget.attrs['class'] = 'form-control'
        self.fields['room_number'].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control'
        self.fields['health_info'].widget.attrs['class'] = 'form-control'
        self.fields['observations'].widget.attrs['class'] = 'form-control'


class ObservationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['observations']
        labels = {
            'observations': ''
        }
        help_texts = {
            'observations': 'Jakákoliv vypozorovaná zajímavá fakta ke klientovi (např. zájmy, oblícená témata a aktivty atd.)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observations'].widget.attrs['class'] = 'form-control'


class InstituteContactForm(forms.ModelForm):
    class Meta:
        model = Institute_contact
        fields = ['name', 'phone_number', 'email']
        labels = {
            'name': 'Celé jméno',
            'phone_number': 'Telefonní číslo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'zip_code', 'city']
        labels = {
            'street': 'Ulice',
            'zip_code': 'PSČ',
            'city': 'Město'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['street'].widget.attrs['class'] = 'form-control'
        self.fields['zip_code'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'


class DayScheduleForm(forms.ModelForm):
    class Meta:
        model = DaySchedule
        fields = ['time', 'description']
        labels = {
            'time': 'Čas',
            'description': 'Popis'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


# tady jsem chtela pridat widget na DateTime aby admin nemusel komplikovane zadavat to 'Smazat k datu',
# bohuzel se to pak vsechno zkomplikovalo s vkladanim dat existujicich oznameni
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['text', 'delete_date', 'delete_time']
        labels = {
            'text': 'Text',
            'delete_date': 'Smazat k datu a času'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['delete_date'].widget.attrs['class'] = 'form-control'
        self.fields['delete_time'].widget.attrs['class'] = 'form-control'


