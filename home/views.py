from django.db import transaction
from django.db.models.signals import post_save
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from caregiver.models import Caregiver
from patient.models import Patient, MedicationIntake, Contact
from .decorators import admin_required
from .forms import RegisterUserForm, PatientForm, ContactForm, MedicationIntakeForm, UpdateUsersInformationForm, \
    ResetUserPasswordForm, UpdatePatientForm


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
            elif user.groups.filter(name='Patients').exists():
                return redirect('index_patient')
            else:
                messages.success(request, 'Obraťte se na IT podporu.')
                return redirect('login_user')

        else:
            messages.success(request,
                             'Účet s těmito údaji neexistuje, zkuste se přihlásit znovu nebo se obraťe na IT podporu.')
            return redirect('login_user')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně')
    return redirect('index')


@admin_required
def administration(request):
    return render(request, 'administration.html')


@admin_required
def account_creation(request):
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Vytvoření účtu proběhlo úspěšně')

        selected_group = form.cleaned_data['groups']
        if selected_group.name == 'Patients':
            return redirect('patient_registration')
        elif selected_group.name == 'Caregivers':
            Caregiver.objects.create(user=user)
            return redirect('administration')
        else:
            return redirect('administration')
    else:
        return render(request, 'acc_creation.html', {'form': form})


# @admin_required
# def register_patient(request):
#     ContactFormSet = modelformset_factory(Contact, form=ContactForm, extra=0)
#     MedicationFormSet = modelformset_factory(MedicationIntake, form=MedicationIntakeForm, extra=0)
#
#     if request.method == 'POST':
#         patient_form = PatientForm(request.POST)
#         contact_formset = ContactFormSet(request.POST, prefix='contacts')
#         medication_formset = MedicationFormSet(request.POST, prefix='medications')
#
#         if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
#             with transaction.atomic():
#                 patient = patient_form.save()
#
#                 for contact_form in contact_formset:
#                     if contact_form.has_changed():
#                         contact = contact_form.save(commit=False)
#                         contact.patient = patient
#                         contact.save()
#
#                 for medication_form in medication_formset:
#                     if medication_form.has_changed():
#                         medication = medication_form.save(commit=False)
#                         medication.patient = patient
#                         medication.save()
#
#             messages.success(request, 'Registrace klienta proběhla úspěšně')
#             return redirect('administration')
#
#     else:
#         patient_form = PatientForm()
#         contact_formset = ContactFormSet(queryset=Contact.objects.none(), prefix='contacts')
#         medication_formset = MedicationFormSet(queryset=MedicationIntake.objects.none(), prefix='medications')
#
#     return render(request, 'register_patient.html', {
#         'patient_form': patient_form,
#         'contact_formset': contact_formset,
#         'medication_formset': medication_formset,
#     })


@admin_required
def display_users(request):
    users = User.objects.all()

    patients = []
    caregivers = []
    admins = []
    unfinished_users = []
    for user in users:
        if getattr(user, 'patient_profile', None):
            patients.append(user.patient_profile)
        elif 'Caregivers' in user.groups.values_list('name', flat=True):
            caregivers.append(user)
        elif 'Admins' in user.groups.values_list('name', flat=True):
            admins.append(user)
        elif 'Patients' in user.groups.values_list('name', flat=True):
            unfinished_users.append(user)

    context = {
        'patients': patients,
        'caregivers': caregivers,
        'admins': admins,
        'unfinished_users': unfinished_users,
    }

    return render(request, 'display_users.html', context)


@admin_required
def user_update(request, info_on_user):
    group, first_name, last_name = info_on_user.split('-')
    # TODO: osetrit uzivatele se stejnym krestnim jmenem a prijemenim?
    user = User.objects.get(first_name=first_name, last_name=last_name)
    form = UpdateUsersInformationForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        messages.success(request, 'Informace byly ulozeny!')
        return redirect('display_users')
    else:
        return render(request, 'user_update.html', {'user': user, 'group': group, 'form': form})


@admin_required
def user_reset_password(request, info_on_user):
    group, first_name, last_name = info_on_user.split('-')
    user = User.objects.get(first_name=first_name, last_name=last_name)
    form = ResetUserPasswordForm(user, request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Heslo bylo zmeneno!')
        return redirect('user_update', info_on_user)

    else:
        return render(request, 'user_reset_password.html', {'form': form, 'info_on_user': info_on_user})


# @admin_required
# def patient_update(request, info_on_user):
#     group, first_name, last_name = info_on_user.split('-')
#     patient = User.objects.get(first_name=first_name, last_name=last_name).patient_profile
#
#     ContactFormSet = inlineformset_factory(Patient, Contact, form=ContactForm, extra=0, can_delete=True)
#     MedicationFormSet = inlineformset_factory(Patient, MedicationIntake, form=MedicationIntakeForm, extra=0,
#                                               can_delete=True)
#
#     if request.method == 'POST':
#         patient_form = UpdatePatientForm(request.POST, instance=patient)
#         contact_formset = ContactFormSet(request.POST, instance=patient)
#         medication_formset = MedicationFormSet(request.POST, instance=patient)
#
#         if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
#             with transaction.atomic():
#                 patient = patient_form.save()
#
#                 for contact_form in contact_formset:
#                     if contact_form.has_changed():
#                         contact = contact_form.save(commit=False)
#                         contact.patient = patient
#                         contact.save()
#
#                 for medication_form in medication_formset:
#                     if medication_form.has_changed():
#                         medication = medication_form.save(commit=False)
#                         medication.patient = patient
#                         medication.save()
#
#             contact_formset.save()
#             medication_formset.save()
#
#             messages.success(request, 'Patient information updated successfully.')
#             return redirect('administration')
#         else:
#             messages.error(request, 'There was an error updating the patient information. Please check the form.')
#
#     else:
#         patient_form = UpdatePatientForm(instance=patient)
#         patient_form.initial['date_of_admission'] = patient.date_of_admission.strftime('%Y-%m-%d')
#         patient_form.initial['birthday'] = patient.birthday.strftime('%Y-%m-%d')
#         contact_formset = ContactFormSet(instance=patient)
#         medication_formset = MedicationFormSet(instance=patient)
#
#     return render(request, 'universal_patient_form.html', {
#         'patient_form': patient_form,
#         'contact_formset': contact_formset,
#         'medication_formset': medication_formset,
#         'creating': False
#     })


# TODO: hezci moznost odstraneni existujicich kontaktu pacienta pri uprave infa

def universal_patient_form(request, info_on_user=None):
    if info_on_user:
        # Handle patient update
        group, first_name, last_name = info_on_user.split('-')
        patient = User.objects.get(first_name=first_name, last_name=last_name).patient_profile

        ContactFormSet = inlineformset_factory(Patient, Contact, form=ContactForm, extra=0, can_delete=True)
        MedicationFormSet = inlineformset_factory(Patient, MedicationIntake, form=MedicationIntakeForm, extra=0,
                                                  can_delete=True)

        if request.method == 'POST':
            patient_form = UpdatePatientForm(request.POST, instance=patient)
            contact_formset = ContactFormSet(request.POST, instance=patient, prefix='contacts')
            medication_formset = MedicationFormSet(request.POST, instance=patient, prefix='medications')

            if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
                with transaction.atomic():
                    patient = patient_form.save()

                    for contact_form in contact_formset:
                        if contact_form.has_changed():
                            contact = contact_form.save(commit=False)
                            contact.patient = patient
                            contact.save()

                    for medication_form in medication_formset:
                        if medication_form.has_changed():
                            medication = medication_form.save(commit=False)
                            medication.patient = patient
                            medication.save()

                contact_formset.save()
                medication_formset.save()

                messages.success(request, 'Patient information updated successfully.')
                return redirect('administration')
            else:
                messages.error(request, 'There was an error updating the patient information. Please check the form.')

        else:
            patient_form = UpdatePatientForm(instance=patient)
            patient_form.initial['date_of_admission'] = patient.date_of_admission.strftime('%Y-%m-%d')
            patient_form.initial['birthday'] = patient.birthday.strftime('%Y-%m-%d')
            contact_formset = ContactFormSet(instance=patient, prefix='contacts')
            medication_formset = MedicationFormSet(instance=patient, prefix='medications')

        creating = False
    else:
        # Handle patient registration
        ContactFormSet = modelformset_factory(Contact, form=ContactForm, extra=0)
        MedicationFormSet = modelformset_factory(MedicationIntake, form=MedicationIntakeForm, extra=0)

        if request.method == 'POST':
            patient_form = PatientForm(request.POST)
            contact_formset = ContactFormSet(request.POST, prefix='contacts')
            medication_formset = MedicationFormSet(request.POST, prefix='medications')

            if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
                with transaction.atomic():
                    patient = patient_form.save()

                    for contact_form in contact_formset:
                        if contact_form.has_changed():
                            contact = contact_form.save(commit=False)
                            contact.patient = patient
                            contact.save()

                    for medication_form in medication_formset:
                        if medication_form.has_changed():
                            medication = medication_form.save(commit=False)
                            medication.patient = patient
                            medication.save()

                messages.success(request, 'Registrace klienta proběhla úspěšně')
                return redirect('administration')

        else:
            patient_form = PatientForm()
            contact_formset = ContactFormSet(queryset=Contact.objects.none(), prefix='contacts')
            medication_formset = MedicationFormSet(queryset=MedicationIntake.objects.none(), prefix='medications')

        creating = True

    return render(request, 'universal_patient_form.html', {
        'patient_form': patient_form,
        'contact_formset': contact_formset,
        'medication_formset': medication_formset,
        'creating': creating
    })
