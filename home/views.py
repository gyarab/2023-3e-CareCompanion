from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .decorators import admin_required
from .forms import RegisterUserForm, PatientForm, CaregiverForm


def index(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Admins').exists():
                return redirect('administration')
            elif user.groups.filter(name='Caregivers').exists():
                return redirect('index_caregiver')
            else:
                return redirect('index_patient')

        else:
            messages.success(request,
                             'Při přihlašování nastala chyba, znova si zkontrolujte zadané údaje, případně se obraťte '
                             'na IT podporu. ')
            return redirect('login_user')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně')
    return redirect('index')


@admin_required
def administration(request):
    return render(request, 'administration.html')


@admin_required
def account_creation(request):
    if request.method == 'POST':
        path = request.path
        if 'opatrovnika' in path:
            print('yur')
        else:
            pass
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrace proběhla úspěšně')
            return redirect('login_user')

    else:
        form = RegisterUserForm()

    return render(request, 'acc_creation.html', {'form': form})


@admin_required
def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration')  # Redirect to a success page or wherever you prefer
    else:
        form = PatientForm()

    return render(request, 'register_patient.html', {'form': form})

# ContactFormSet = inlineformset_factory(Patient, Contact, fields=('relationship', 'name', 'phone_number'), extra=1)
# MedicationIntakeFormSet = inlineformset_factory(Patient, MedicationIntake, fields=('medication', 'when', 'how'), extra=1)

@admin_required
def register_caregiver(request):
    if request.method == 'POST':
        form = CaregiverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration')  # Redirect to a success page or wherever you prefer
    else:
        form = CaregiverForm()

    return render(request, 'register_caregiver.html', {'form': form})

# @admin_required
# def register_patient(request):
#     if request.method == 'POST':
#         patient_form = PatientForm(request.POST)
#         contact_formset = ContactFormSet(request.POST, prefix='contact')
#         medication_formset = MedicationIntakeFormSet(request.POST, prefix='medication')
#
#         if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
#             patient = patient_form.save(commit=False)  # Don't save to the database yet
#             patient.user = request.user  # Set the user for the patient
#             patient.save()  # Now save to the database
#
#             contact_formset.instance = patient
#             contact_formset.save()
#             medication_formset.instance = patient
#             medication_formset.save()
#             return redirect('success_page')
#
#     else:
#         patient_form = PatientForm()
#         contact_formset = ContactFormSet(prefix='contact')
#         medication_formset = MedicationIntakeFormSet(prefix='medication')
#
#     return render(request, 'register_patient.html', {
#         'patient_form': patient_form,
#         'contact_formset': contact_formset,
#         'medication_formset': medication_formset,
#     })

# @admin_required
# def register_user(request):
#     path = request.path
#     if request.method == 'POST':
#         if 'opatrovnik' in path:
#             form = RegistrationCaregiverForm(request.POST)
#         else:
#             form = RegistrationPatientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registrace proběhla úspěšně')
#             return redirect('login_user')
#
#     else:
#         if 'opatrovnik' in path:
#             form = RegistrationCaregiverForm()
#         else:
#             form = RegistrationPatientForm()
#
#     return render(request, 'acc_creation.html', {'form': form,
#                                                  'caregiver': 'opatrovnik' in path})
