from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .models import Contact as Institute_contact, Address, DaySchedule, Announcement
from caregiver.models import Caregiver
from patient.models import Patient, MedicationIntake, Contact as Patient_contact, Activity
from .decorators import admin_required
from .forms import RegisterUserForm, PatientForm, PatientContactForm, MedicationIntakeForm, UpdateUsersInformationForm, \
    ResetUserPasswordForm, UpdatePatientForm, InstituteContactForm, AddressForm, DayScheduleForm, AnnouncementForm, \
    PatientActivityForm


def index(request):
    context = {
        'contacts': Institute_contact.objects.all(),
        'address': Address.objects.first()
    }

    if request.user.is_authenticated:
        now = timezone.now()
        upc_announcements = Announcement.objects.filter(
            Q(delete_date__gt=now.date()) |  # skonci v budoucnu
            (Q(delete_date=now.date()) & Q(delete_time__gt=now.time()))  # dnesni co jeste nemaji byt mazany
        )
        delete_from_database(Announcement.objects.all(), upc_announcements)

        context.update({
            'day_schedules': DaySchedule.objects.all().order_by('time'),
            'announcements': upc_announcements
        })
        return render(request, 'loggedin_homepage.html', context)
    else:
        return render(request, 'default_homepage.html', context)


def delete_from_database(arr_w_all_objs, arr_w_upc_objs):
    objs_for_deletion = arr_w_all_objs.exclude(id__in=[obj.id for obj in arr_w_upc_objs])
    objs_for_deletion.delete()


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


# TODO: hezci moznost odstraneni existujicich kontaktu pacienta pri uprave infa

@admin_required
def universal_patient_form(request, info_on_user=None):
    if info_on_user:
        # Handle patient update
        group, first_name, last_name = info_on_user.split('-')
        patient = User.objects.get(first_name=first_name, last_name=last_name).patient_profile

        ContactFormSet = inlineformset_factory(Patient, Patient_contact, form=PatientContactForm, extra=0,
                                               can_delete=True)
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
        ContactFormSet = modelformset_factory(Patient_contact, form=PatientContactForm, extra=0)
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
            contact_formset = ContactFormSet(queryset=Patient_contact.objects.none(), prefix='contacts')
            medication_formset = MedicationFormSet(queryset=MedicationIntake.objects.none(), prefix='medications')

        creating = True

    return render(request, 'universal_patient_form.html', {
        'patient_form': patient_form,
        'contact_formset': contact_formset,
        'medication_formset': medication_formset,
        'creating': creating
    })


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
def institute_info(request):
    contacts = Institute_contact.objects.all()
    address = Address.objects.first()
    day_schedules = DaySchedule.objects.all()
    announcements = Announcement.objects.all()

    context = {
        'contacts': contacts,
        'address': address,
        'day_schedules': day_schedules,
        'announcements': announcements
    }

    return render(request, 'institute_info.html', context)


@admin_required
def edit_institute_info(request, category):
    category_map = {
        'kontakty': (InstituteContactForm, Institute_contact, 'Kontakty'),
        'adresa': (AddressForm, Address, 'Adresa'),
        'denni-rozvrh': (DayScheduleForm, DaySchedule, 'Denní rozvrh'),
        'oznameni': (AnnouncementForm, Announcement, 'Oznamení'),
    }
    form, model, header = category_map.get(category)

    formset_class = modelformset_factory(model, form=form, extra=0, can_delete=True)
    queryset = model.objects.all()
    formset = formset_class(request.POST or None, queryset=queryset)

    if category == 'oznameni':
        for form, obj in zip(formset, queryset):
            form.initial['delete_date'] = obj.delete_date.strftime('%Y-%m-%d')

    if formset.is_valid():
        formset.save()
        messages.success(request, 'Informace byly ulozeny!')
        return redirect('institute_info')
    else:
        return render(request, 'edit_institute_info.html', {'formset': formset, 'header': header})


@admin_required
def shifts(request):
    caregivers = Caregiver.objects.all()
    return render(request, 'shifts.html', {'caregivers': caregivers})


@admin_required
def edit_shifts(request, pk):
    caregiver = Caregiver.objects.get(pk=pk)
    return render(request, 'edit_shifts.html', {'caregiver': caregiver})


@admin_required
def patient_activities(request):
    patients = Patient.objects.all()
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
    else:
        return render(request, 'edit_patient_activities.html', {'patient': patient, 'formset': formset})
