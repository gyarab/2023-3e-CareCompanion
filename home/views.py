from django.db import transaction
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from caregiver.models import Caregiver, Shift
from patient.models import Patient, MedicationIntake, Contact, Activity
from .decorators import admin_required
from .forms import RegisterUserForm, PatientForm, PatientContactForm, MedicationIntakeForm, UpdateUsersInformationForm, \
    ResetUserPasswordForm, UpdatePatientForm, PatientActivityForm, CaregiverShiftForm


def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Admins').exists():
            return redirect('administration')
        elif request.user.groups.filter(name='Caregivers').exists():
            return redirect('index_caregiver')
        elif request.user.groups.filter(name='Patients').exists():
            return redirect('index_patient')
    else:
        return render(request, 'homepage.html')


def delete_from_database(arr_w_all_objs, arr_w_upc_objs):
    objs_for_deletion = arr_w_all_objs.exclude(id__in=[obj.id for obj in arr_w_upc_objs])
    objs_for_deletion.delete()


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
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
    return redirect('login_user')


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
        if selected_group == 'Patients':
            return redirect('patient_registration')
        elif selected_group == 'Caregivers':
            Caregiver.objects.create(user=user)
            return redirect('administration')
        else:
            return redirect('administration')

    else:
        return render(request, 'acc_creation.html', {'form': form})


@admin_required
def display_users(request):
    patients = []
    caregivers = []
    admins = []
    unfinished_users = []
    users = User.objects.all().order_by('last_name')

    for user in users:
        groups = user.groups.values_list('name', flat=True)

        if getattr(user, 'patient_profile', None):
            patients.append(user)
        elif 'Caregivers' in groups:
            caregivers.append(user)
        elif 'Admins' in groups:
            admins.append(user)
        elif 'Patients' in groups:
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
    user = User.objects.get(first_name=first_name, last_name=last_name)
    form = UpdateUsersInformationForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        messages.success(request, 'Informace byly uloženy!')
        return redirect('display_users')

    context = {
        'user': user,
        'group': group,
        'form': form
    }

    return render(request, 'user_update.html', context)


@admin_required
def user_reset_password(request, info_on_user):
    group, first_name, last_name = info_on_user.split('-')
    user = User.objects.get(first_name=first_name, last_name=last_name)
    form = ResetUserPasswordForm(user, request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Heslo bylo zmeneno!')
        return redirect('user_update', info_on_user)

    context = {
        'form': form,
        'info_on_user': info_on_user
    }

    return render(request, 'user_reset_password.html', context)


@admin_required
def universal_patient_form(request, info_on_user=None):
    if info_on_user:
        group, first_name, last_name = info_on_user.split('-')
        patient = User.objects.get(first_name=first_name, last_name=last_name).patient_profile

        ContactFormSet = inlineformset_factory(Patient, Contact, form=PatientContactForm, extra=0, can_delete=True)
        MedicationFormSet = inlineformset_factory(Patient, MedicationIntake, form=MedicationIntakeForm, extra=0, can_delete=True)

        patient_form = UpdatePatientForm(request.POST or None, instance=patient)
        contact_formset = ContactFormSet(request.POST or None, instance=patient, prefix='contacts')
        medication_formset = MedicationFormSet(request.POST or None, instance=patient, prefix='medications')

        if all(form.is_valid() for form in (patient_form, contact_formset, medication_formset)):
            save_patients_info(patient_form, contact_formset, medication_formset)

            messages.success(request, 'Klientovi informace byly úspěšně uloženy')
            return redirect('display_users')

        patient_form.initial['date_of_admission'] = patient.date_of_admission.strftime('%Y-%m-%d')
        patient_form.initial['birthday'] = patient.birthday.strftime('%Y-%m-%d')
        creating = False

    else:
        ContactFormSet = modelformset_factory(Contact, form=PatientContactForm, extra=0)
        MedicationFormSet = modelformset_factory(MedicationIntake, form=MedicationIntakeForm, extra=0)

        patient_form = PatientForm(request.POST or None)
        contact_formset = ContactFormSet(request.POST or None, prefix='contacts')
        medication_formset = MedicationFormSet(request.POST or None, prefix='medications')

        if all(form.is_valid() for form in (patient_form, contact_formset, medication_formset)):
            save_patients_info(patient_form, contact_formset, medication_formset)

            messages.success(request, 'Registrace klienta proběhla úspěšně')
            return redirect('administration')

        contact_formset.queryset = Contact.objects.none()
        medication_formset.queryset = MedicationIntake.objects.none()
        creating = True

    context = {
        'patient_form': patient_form,
        'contact_formset': contact_formset,
        'medication_formset': medication_formset,
        'creating': creating
    }

    return render(request, 'universal_patient_form.html', context)


def save_patients_info(patient_form, contact_formset, medication_formset):
    with transaction.atomic():
        patient = patient_form.save()

        for formset in (contact_formset, medication_formset):
            for form in formset:
                if form.has_changed():
                    instance = form.save(commit=False)
                    instance.patient = patient
                    instance.save()

                formset.save()


@admin_required
def delete_user(request, pk):
    user_for_deletion = User.objects.get(pk=pk)
    if request.method == 'POST':
        user_for_deletion.delete()
        return redirect('display_users')

    context = {
        'first_name': user_for_deletion.first_name,
        'last_name': user_for_deletion.last_name
    }
    return render(request, 'delete_user.html', context)


@admin_required
def shifts(request):
    caregivers = Caregiver.objects.all().order_by('user__last_name')
    return render(request, 'shifts.html', {'caregivers': caregivers})


@admin_required
def edit_shifts(request, pk):
    caregiver = Caregiver.objects.get(pk=pk)
    shifts = Shift.objects.all().filter(caregiver=caregiver)

    formset_class = modelformset_factory(Shift, form=CaregiverShiftForm, extra=0, can_delete=True)
    formset = formset_class(request.POST or None, queryset=shifts)
    for form, obj in zip(formset, shifts):
        form.initial['date_of_shift'] = obj.date_of_shift.strftime('%Y-%m-%d')

    if formset.is_valid():
        for form in formset:
            if form.has_changed():
                shift = form.save(commit=False)
                shift.caregiver = caregiver
                shift.save()

        formset.save()
        messages.success(request, 'Informace byly úspěšně uloženy')
        return redirect('shifts')

    context = {
        'caregiver': caregiver,
        'formset': formset
    }

    return render(request, 'edit_shifts.html', context)


@admin_required
def patient_activities(request):
    patients = Patient.objects.all().order_by('user__last_name')
    return render(request, 'patient_activities.html', {'patients': patients})


@admin_required
def edit_patient_activities(request, pk):
    patient = Patient.objects.get(pk=pk)
    activities = Activity.objects.all().filter(patient=patient)

    formset_class = modelformset_factory(Activity, form=PatientActivityForm, extra=0, can_delete=True)
    formset = formset_class(request.POST or None, queryset=activities)
    for form, obj in zip(formset, activities):
        form.initial['date'] = obj.date.strftime('%Y-%m-%d')

    if formset.is_valid():
        for form in formset:
            if form.has_changed():
                activity = form.save(commit=False)
                activity.patient = patient
                activity.save()

        formset.save()
        messages.success(request, 'Informace byly ulozeny!')
        return redirect('patient_activities')

    context = {
        'patient': patient,
        'formset': formset
    }

    return render(request, 'edit_patient_activities.html', context)
