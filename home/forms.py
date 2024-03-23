from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django import forms

from caregiver.models import Caregiver
from patient.models import Patient, Contact, MedicationIntake


class RegisterUserForm(UserCreationForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select,
        required=True,
    )

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('groups', 'first_name', 'last_name', 'username', 'password1', 'password2')

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
    )

    class Meta:
        model = Patient
        fields = ['user', 'date_of_admission', 'room_number', 'birthday', 'health_info', 'fav_activities']
        widgets = {
            'user': forms.Select(),
            'date_of_admission': DateInput(),
            'birthday': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_admission'].widget.attrs['class'] = 'form-control'
        self.fields['room_number'].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control'
        self.fields['health_info'].widget.attrs['class'] = 'form-control'
        self.fields['fav_activities'].widget.attrs['class'] = 'form-control'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['relationship', 'name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['relationship'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'


class MedicationIntakeForm(forms.ModelForm):
    class Meta:
        model = MedicationIntake
        fields = ['medication', 'when', 'how']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medication'].widget.attrs['class'] = 'form-control'
        self.fields['when'].widget.attrs['class'] = 'form-control'
        self.fields['how'].widget.attrs['class'] = 'form-control'


class CaregiverForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Caregivers').exclude(caregiver_profile__isnull=False),
        widget=forms.Select,
        required=True,
    )

    class Meta:
        model = Caregiver
        fields = ['user', 'start_date']
        widgets = {
            'start_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'form-control'
        self.fields['start_date'].widget.attrs['class'] = 'form-control'


class UpdateUsersInformationForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'


class ResetUserPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
