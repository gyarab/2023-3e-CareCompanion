from datetime import datetime, timedelta
from babel.dates import format_date

from django.db.models import Q, F, ExpressionWrapper, BooleanField
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from home.decorators import caregiver_required
from patient.models import Patient, Activity
from home.forms import ObservationForm, PatientActivityForm


# Home opatrovníka
# Zobrazí celé jméno přihlášeného opatrovníka a výběr z funkcí aplikace
@caregiver_required
def index(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {
        'first_name': first_name,
        'last_name': last_name
    }
    return render(request, 'index_caregiver.html', context)


# Zdravotní karty klientů
# Zobrazí jména všech registrovaných klientů, výběr konkrétního
# Možnost hledání podle jména a čísla pokoje
@caregiver_required
def medical_cards(request):
    patients = Patient.objects.all().order_by('user__last_name')
    return render(request, 'medical_cards.html', {'patients': patients})


# Zdravotní karta konktrétního klienta
# Zobrazí info o klientovi - možnost změny postřehů
@caregiver_required
def patient_info(request, full_name_of_patient):
    first_name, last_name = full_name_of_patient.split('-')
    # Z url zjistíme křestní a příjmení -> konkrétní klient
    patient = Patient.objects.get(user__first_name=first_name, user__last_name=last_name)
    # Formulář pro vyplňování postřehů
    form = ObservationForm(request.POST or None, instance=patient)

    if form.is_valid():
        form.save()
        # Po úspěšném uložení změn je uživatel přesměrován na stejnou stránku - zobrazí aktualizované info
        return redirect('patient_info', full_name_of_patient)

    context = {
        'patient': patient,
        'form': form
    }

    return render(request, 'patient_info.html', context)


# Směny přihlášeného opatrovníka
# Zobrazí probíhající a nastávající směny
# Dnešní směny jsou graficky odlišné od těch ostatních
@caregiver_required
def shift_schedule(request):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    caregiver = request.user.caregiver_profile
    context = {'caregiver': caregiver}

    # Query s relevantními směnami
    shifts_to_display = caregiver.shift_set.annotate(
        # is_overnight bude True pokud:
        # 1) Datum směny je včerejší, čas začátku směny je větší než čas konce (přes půlnoc)
        # a čas konce směny je větší než současný čas (ještě neskončila)
        # 2) Datum směny je dnešní a čas začátku směny je větší než čas konce (přes půlnoc)
        # (není potřeba kontrolovat zda skončila, jelikož začala dnes a bude končit urřitě zítra)
        is_overnight=ExpressionWrapper(
            (Q(date_of_shift=yesterday) & Q(start__gt=F('end')) & Q(end__gt=now.time())) |
            (Q(date_of_shift=now.date()) & Q(start__gt=F('end'))),
            output_field=BooleanField()
        )

    # Načte směny, které odpovídají aspoň jedné z těchto podmínek:
    # 1) Datum směny je větší než aktuální datum (směna v budoucnu)
    # 2) is_overnight je True (vysvětleno nahoře)
    # 3) Směna je dnes a ještě neskončila
    ).filter(
        Q(date_of_shift__gt=now.date()) |
        Q(is_overnight=True) |
        (Q(date_of_shift=now.date()) & Q(end__gt=now.time()))
    ).order_by('date_of_shift', 'start')

    # Při příležitosti toho, že máme v array uložené všechny relevantní směny z databáze, smažeme všechny ostatní
    delete_from_database(caregiver.shift_set.filter(caregiver=caregiver), shifts_to_display)

    # Jestli má opatrovník relevantní směny
    if shifts_to_display:
        context.update({'any_shifts': True})
        soonest_shift = shifts_to_display.first()
        shift_start = datetime.combine(soonest_shift.date_of_shift, soonest_shift.start)
        shift_end = datetime.combine(soonest_shift.date_of_shift, soonest_shift.end)

        # Jestli je nejbližší směna dnešní, zobrazíme ji graficky odděleně
        if shift_start <= now <= shift_end or soonest_shift.is_overnight_shift():
            context.update({
                'today': True,
                'shift_start': shift_start.time,
                'shift_end': shift_end.time
            })

            # Jestli dnešní existuje, pole relevantních směn nastavíme až od té druhé nejbližší, jelikož ta dnešní je
            # zobrazena odděleně
            shifts_to_display = shifts_to_display[1:]

        # Uložení informací o každé z nadcházejících směn
        if shifts_to_display:
            upcoming_shifts_info = []
            for upcoming_shift in shifts_to_display:
                upcoming_shifts_info.append({
                    # Formátování datumu do češtiny a s dnem v týdnu
                    'upcom_shift_date': format_date(upcoming_shift.date_of_shift, format='EEEE d. MMMM',
                                                    locale='cs_CZ'),
                    'upcom_shift_start': upcoming_shift.start,
                    'upcom_shift_end': upcoming_shift.end
                })

            context.update({'upcoming_shifts_info': upcoming_shifts_info})

    # Jestli nemá relevantní směny
    else:
        context.update({'any_shifts': False})

    return render(request, 'shift_schedule.html', context)


# Funkce, která bere 2 argumenty:
# 'arr_w_all_objs' = pole se všemi objekty
# 'arr_w_upc_objs' = pole pouze s několika objekty z prvního pole
# Je vytvořeno pole 'objs_for_deletion' s objekty, které se nachází v 'arr_w_all_objs' ,ale ne v 'arr_w_upc_objs'
# Tato funkce je využita na mazání irelavantních směn a rozvrhů z databáze
def delete_from_database(arr_w_all_objs, arr_w_upc_objs):
    objs_for_deletion = arr_w_all_objs.exclude(id__in=[obj.id for obj in arr_w_upc_objs])
    objs_for_deletion.delete()


# Rozvrhy dne všech klientů
# Zobrazí klienty a jejich rozvrhy, možnost přesměrování za účelem úpravy rozvrhů konkrétního klienta
@caregiver_required
def patient_schedules(request):
    now = datetime.now()
    patients = Patient.objects.all().order_by('user__last_name')
    patients_info = []

    # Do pole 'patients_info' se načtou všichni registrovaní klienti a jejich rozvrhy
    for patient in patients:
        todays_activities = []
        other_activities = []
        # Pole s relevantními rozvrhy - ty s dnešním a budoucím datumem
        activities = patient.activity_set.filter(date__gte=now.date())
        # Irelevantní rozvrhy smažeme z databáze
        delete_from_database(patient.activity_set.filter(patient=patient), activities)

        for activity in activities:
            if activity.date == now.date():
                todays_activities.append({'activity': activity})
            else:
                # Jestli rozvrh není dnešní zobrazujeme jeho datum - tímto řádkem se formátuje (do čj + den v týdnu)
                activity.date = format_date(activity.date, format='EEEE d. MMMM', locale='cs_CZ')
                other_activities.append({'activity': activity})

        patients_info.append({
            'patient': patient,
            'todays_activities': todays_activities,
            'other_activities': other_activities
        })

    context = {'patients_info': patients_info}

    return render(request, 'patient_schedules.html', context)


# Úprava rozvrhu konkrétního klienta
# Možnost přidání nových rozvrhů a mazání/úpravy již existujících
@caregiver_required
def edit_patient_schedules(request, pk):
    # Získání konkrétního pacienta a jeho rozvrhů přes primary key
    patient = Patient.objects.get(pk=pk)
    activities = Activity.objects.all().filter(patient=patient)

    formset_class = modelformset_factory(Activity, form=PatientActivityForm, extra=0, can_delete=True)
    formset = formset_class(request.POST or None, queryset=activities)
    # Formátování datumů již vytvořených rozvrhů aby se data dobře vložila do formuláře
    for form, obj in zip(formset, activities):
        form.initial['date'] = obj.date.strftime('%Y-%m-%d')

    if formset.is_valid():
        for form in formset:
            if form.has_changed():
                activity = form.save(commit=False)
                activity.patient = patient
                activity.save()

        formset.save()
        return redirect('patient_schedules')

    context = {
        'patient': patient,
        'formset': formset
    }

    return render(request, 'edit_patient_schedules.html', context)


# Příručka
@caregiver_required
def manual(request):
    return render(request, 'manual.html')


@caregiver_required
def what_to_do(request):
    return render(request, 'what_to_do.html')


@caregiver_required
def free_time_activities(request):
    return render(request, 'free_time_activities.html')


@caregiver_required
def education(request):
    return render(request, 'education.html')
