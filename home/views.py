from django.db import transaction
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from patient.models import Patient, MedicationIntake, Contact
from .decorators import admin_required
from .forms import RegisterUserForm, PatientForm, CaregiverForm, ContactForm, MedicationIntakeForm


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
    ContactFormSet = modelformset_factory(Contact, form=ContactForm, extra=0)
    MedicationFormSet = modelformset_factory(MedicationIntake, form=MedicationIntakeForm, extra=0)

    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        contact_formset = ContactFormSet(request.POST, prefix='contacts')
        medication_formset = MedicationFormSet(request.POST, prefix='medications')
        print("Patient form is valid:", patient_form.is_valid())
        print("Contact form is valid:", contact_formset.is_valid())
        print("Med form is valid:", medication_formset.is_valid())

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

            return redirect('administration')

    else:
        patient_form = PatientForm()
        contact_formset = ContactFormSet(queryset=Contact.objects.none(), prefix='contacts')
        medication_formset = MedicationFormSet(queryset=MedicationIntake.objects.none(), prefix='medications')

    return render(request, 'register_patient.html', {
        'patient_form': patient_form,
        'contact_formset': contact_formset,
        'medication_formset': medication_formset,
    })


@admin_required
def register_caregiver(request):
    if request.method == 'POST':
        form = CaregiverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration')
    else:
        form = CaregiverForm()

    return render(request, 'register_caregiver.html', {'form': form})
