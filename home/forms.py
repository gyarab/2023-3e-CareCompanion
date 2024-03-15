from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import inlineformset_factory

from caregiver.models import Caregiver
from patient.models import Patient, Contact, MedicationIntake


class RegisterUserForm(UserCreationForm):

    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select,
        required=True,
        help_text="Select the group for the user.",
    )

    first_name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('groups', 'first_name', 'surname','username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data.get('groups')

        if commit:
            user.save()
            user.groups.set([group])
        return user

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'first_name', 'surname', 'date_of_admission', 'room_number', 'birthday', 'health_info', 'fav_activities']
        widgets = {
            'user': forms.Select(),
            'date_of_admission': DateInput(),
            'birthday': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(groups__name='Patients').exclude(
            patient_profile__isnull=False)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['relationship', 'name', 'phone_number']


class MedicationIntakeForm(forms.ModelForm):
    class Meta:
        model = MedicationIntake
        fields = ['medication', 'when', 'how']


class CaregiverForm(forms.ModelForm):
    class Meta:
        model = Caregiver
        fields = ['user', 'first_name', 'surname', 'start_date']
        widgets = {
            'start_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(groups__name='Caregivers').exclude(
            caregiver_profile__isnull=False)
