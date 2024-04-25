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


# Homepage aplikace
# Pokud uživatel není přihlášený, tak se mu zobrazí homepage aplikace, pokud je, je přesměrován na svůj Home
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


# Přihlášení uživatele
# Jestli je přihlášení úspěšné, uživatel je podle jeho skupiny přesměrován na svoje Home url
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
            # V případě, že uživatel existuje, ale nemá ani jednu ze skupin
            else:
                messages.success(request, 'Obraťte se na IT podporu.')
                return redirect('login_user')

        # V připadě, že uživatel neexistuje
        else:
            messages.success(request,
                             'Účet s těmito údaji neexistuje, zkuste se přihlásit znovu nebo se obraťe na IT podporu.')
            return redirect('login_user')

    else:
        return render(request, 'login.html')


# Odhlášení uživatele
def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně')
    return redirect('login_user')


# Home administrátora
@admin_required
def administration(request):
    return render(request, 'administration.html')


# Tvorba uživatelských účtů
@admin_required
def account_creation(request):
    form = RegisterUserForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        messages.success(request, 'Vytvoření účtu proběhlo úspěšně')

        selected_group = form.cleaned_data['groups']
        # V případě, že vytvořený uživatel je klient, je admin přesměrován na tvorbu klientského profilu
        if selected_group == 'Patients':
            return redirect('patient_registration')
        # Jestli je uživatel opatrovník, vytvoří se objekt Caregiver
        elif selected_group == 'Caregivers':
            Caregiver.objects.create(user=user)
            return redirect('administration')
        else:
            return redirect('administration')

    else:
        return render(request, 'acc_creation.html', {'form': form})


# Zobrazení všech uživatelských účtů
@admin_required
def display_users(request):
    # 4 skupiny podle kterých se uživatelé řadí - klienti, opatrovnící, admini a nedokončení
    # (účty se skupinou 'Patients', ale žádným 'patient_profile' => byl vytvořen uživteslký účet, ale ne profil klienta)
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


# Zobrazení a úprava infa o konkrétním uživatelském účtu
# Možnost změny základních uživatelských informací a hesla, smazání a pokud je to klient, tak změny klientských info
@admin_required
def user_update(request, info_on_user):
    # Z url získáme skupinu, křestní jméno a příjmení konkrétního uživatele
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


# Změna hesla konkrétního uživatele
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


# Univerzální views.py funkce pro tvorbu a úpravu klientských profilů
# Bere argument 'info_on_user'. Jestli není v url zprostředkován, je funkcí definován jako None,
# tak se zjistí, jestli se klient vytváří nebo upravuje
@admin_required
def universal_patient_form(request, info_on_user=None):
    # Jestli 'info_on_user' není None, klient se upravuje
    if info_on_user:
        group, first_name, last_name = info_on_user.split('-')
        patient = User.objects.get(first_name=first_name, last_name=last_name).patient_profile

        # Definice všech potřebných formulářů - formulář pro klienta, kontakty a medikace
        ContactFormSet = inlineformset_factory(Patient, Contact, form=PatientContactForm, extra=0, can_delete=True)
        MedicationFormSet = inlineformset_factory(Patient, MedicationIntake, form=MedicationIntakeForm, extra=0,
                                                  can_delete=True)

        patient_form = UpdatePatientForm(request.POST or None, instance=patient)
        contact_formset = ContactFormSet(request.POST or None, instance=patient, prefix='contacts')
        medication_formset = MedicationFormSet(request.POST or None, instance=patient, prefix='medications')

        # Jestli jsou všechny formuláře validní (admin se snaži něco uložit), všechny se uloží
        if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
            with transaction.atomic():
                patient = patient_form.save()

                # Projde oba formsets kontakty a medikace
                # Podmínky .has_changed() kontrolují zda se formset nějakým způsobem nezměnil
                # V případě těhle formsets (konktakty a medikace) máme možnost přidávat nové formsets
                # Taková akce by triggrovala tuto podmínku a uložila 'nový' formset správně
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

            messages.success(request, 'Klientovi informace byly úspěšně uloženy')
            return redirect('display_users')

        # V případě, že se stránka teprve načítá (nic se neukládá), se správně zformátuje datum,
        # aby se dal vložit do formuláře
        patient_form.initial['birthday'] = patient.birthday.strftime('%Y-%m-%d')
        creating = False

    # V případě, že se klientský profil vytváří, postupuje se podobně, akorát formuláře jsou definovány jinak
    else:
        ContactFormSet = modelformset_factory(Contact, form=PatientContactForm, extra=0)
        MedicationFormSet = modelformset_factory(MedicationIntake, form=MedicationIntakeForm, extra=0)

        patient_form = PatientForm(request.POST or None)
        contact_formset = ContactFormSet(request.POST or None, prefix='contacts')
        medication_formset = MedicationFormSet(request.POST or None, prefix='medications')

        if patient_form.is_valid() and contact_formset.is_valid() and medication_formset.is_valid():
            with transaction.atomic():
                patient = patient_form.save()

                # Projde oba formsets kontakty a medikace
                # Podmínky .has_changed() kontrolují zda se formset nějakým způsobem nezměnil
                # V případě těhle formsets (konktakty a medikace) máme možnost přidávat nové formsets
                # Taková akce by triggrovala tuto podmínku a uložila 'nový' formset správně
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


# Smazání konkrétního uživatele
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


# Směny opatrovníků
# Zobrazí všechny registrované opatrovníky
# Po kliknutí na konkrétního opatrovníka je možnost měnit informace o směnách/přidávat nové
@admin_required
def shifts(request):
    caregivers = Caregiver.objects.all().order_by('user__last_name')
    return render(request, 'shifts.html', {'caregivers': caregivers})


# Úprava směn konkrétního opatrovníka
# Možnost úpravy a mazání již uložených směn a přidání nových
@admin_required
def edit_shifts(request, pk):
    # Díky primary key z url zjistíme opatrovníka i všechny jeho směny
    caregiver = Caregiver.objects.get(pk=pk)
    shifts = Shift.objects.all().filter(caregiver=caregiver)

    formset_class = modelformset_factory(Shift, form=CaregiverShiftForm, extra=0, can_delete=True)
    formset = formset_class(request.POST or None, queryset=shifts)
    for form, obj in zip(formset, shifts):
        # Správné formátování datumů aby data byla vložena do formuláře úspěšně
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


# Rozvrhy klientů
# Zobrazí všechny registrované klienty
# Po kliknutí na konkrétního klienta je možnost měnit informace o rozvrzích/přidávat nové
@admin_required
def patient_activities(request):
    patients = Patient.objects.all().order_by('user__last_name')
    return render(request, 'patient_activities.html', {'patients': patients})


# Úprava rozvrhů konkrétního klienta
# Stejný postup jako ve funkci pro úpravu směn opatrovníků 'edit_shifts'
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
