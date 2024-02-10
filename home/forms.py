from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import inlineformset_factory

from caregiver.models import Caregiver
from patient.models import Patient, Contact, MedicationIntake


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select the groups for the user.",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'groups', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        groups = self.cleaned_data.get('groups')

        if commit:
            user.save()
            user.groups.set(groups)
        return user

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'first_name', 'surname', 'birthday', 'room_number', 'health_info', 'fav_activities']
        widgets = {
            'birthday': forms.TextInput(attrs={'class': 'datepicker'}),
            'user': forms.Select(),  # You can customize this if needed
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
        fields = ['user', 'first_name', 'surname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Patients'))
        self.fields['user'].queryset = User.objects.filter(groups__name='Caregivers').exclude(
            caregiver_profile__isnull=False)
