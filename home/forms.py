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
        # user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Patients'))
        self.fields['user'].queryset = User.objects.filter(groups__name='Patients', patient__isnull=True)


class CaregiverForm(forms.ModelForm):
    class Meta:
        model = Caregiver
        fields = ['user', 'first_name', 'surname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Patients'))
        self.fields['user'].queryset = User.objects.filter(groups__name='Caregivers', caregiver__isnull=True)

        # user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Caregivers'))

# class RegistrationCaregiverForm(forms.ModelForm):
#     # Add additional fields for the user model
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     # Add additional fields for the UserProfile model
#     first_name = forms.CharField(max_length=15)
#     surname = forms.CharField(max_length=20)
#
#     class Meta:
#         model = Caregiver
#         fields = ['username', 'password', 'first_name', 'surname']
#
#
# class RegistrationPatientForm(forms.ModelForm):
#     # Add additional fields for the user model
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     # Add additional fields for the UserProfile model
#     first_name = forms.CharField(max_length=15)
#     surname = forms.CharField(max_length=20)
#
#     class Meta:
#         model = Patient
#         fields = ['username', 'password', 'first_name', 'surname']
