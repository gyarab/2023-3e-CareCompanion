from django.shortcuts import render
from django.db.models import Q, ExpressionWrapper, BooleanField, F
from babel.dates import format_date

from caregiver.models import Caregiver
from home.decorators import patient_required
from datetime import datetime, timedelta


# Home klienta
# Zobrazí dnešní datum a výběr z funkcí aplikace
@patient_required
def index(request):
    date = format_date(datetime.now(), format='EEEE d. MMMM', locale='cs_CZ')
    return render(request, 'index_patient.html', {'date': date})


# Seznam opatrovníku a jejich směny
# Zobrazí tabulku se všemi registrovanými opatrovníky, vedle nich políčko s Ano/Ne, zda jsou na směně.
# Pokud na směně jsou, zobrazí se do kdy. Pokud ne, zobrazí se následující směna.
@patient_required
def caregivers_list(request):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    caregivers_shift_info = []

    # Cyklus projde všechny opatrovníky a uloží ke každému maximálně jednu směnu
    for caregiver in Caregiver.objects.prefetch_related('shift_set').order_by('user__last_name'):

        # První nejbližší relevantní směna
        next_shift = caregiver.shift_set.annotate(
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
        ).order_by('date_of_shift', 'start').first()

        # Pokud opatrovník nějaké směny v databázi má
        if next_shift:
            shift_start = datetime.combine(next_shift.date_of_shift, next_shift.start)
            shift_end = datetime.combine(next_shift.date_of_shift, next_shift.end)

            # Jestli je opatrovník zrovna na směně
            if shift_start <= now <= shift_end or (next_shift.is_overnight_shift() and shift_start <= now):
                caregivers_shift_info.append({
                    'first_name': caregiver.first_name,
                    'last_name': caregiver.last_name,
                    'on_shift': True,
                    'shift_end': next_shift.end,
                })
            # Jestli není
            else:
                # Formátování datumu, které se bude zobrazovat
                next_shift_date = format_date(next_shift.date_of_shift, format='EEEE d. MMMM', locale='cs_CZ')
                caregivers_shift_info.append({
                    'first_name': caregiver.first_name,
                    'last_name': caregiver.last_name,
                    'on_shift': False,
                    'next_shift_date': next_shift_date,
                    'next_shift_start': next_shift.start,
                    'next_shift_end': next_shift.end
                })
        # Pokud nemá žádné směny
        else:
            caregivers_shift_info.append({
                'first_name': caregiver.first_name,
                'last_name': caregiver.last_name,
                'on_shift': False,
                'no_upc_shifts': True
            })

    context = {'caregivers_shift_info': caregivers_shift_info}

    return render(request, 'caregivers_list.html', context)


# Zobrazení kontaktů na blízké
@patient_required
def contacts(request):
    patient = request.user.patient_profile
    return render(request, 'contacts.html', {'patient': patient})


# Rozvrhy dnů
# Zobrazí všechny dnešní a budoucí rozvrhy
@patient_required
def day_schedule(request):
    patient = request.user.patient_profile
    now = datetime.now()
    # Pole obsahující akticity s dnešním a budoucím datem
    activities = patient.activity_set.filter(date__gte=now.date())

    if activities:
        # Rozdělíme aktivity s dnešním a budoucím datem kvuli grafickému rozhraní
        todays_activities = []
        other_activities = []

        for activity in activities:
            if activity.date == now.date():
                todays_activities.append({'activity': activity})
            else:
                # Formátování datumu do čj a s dnem v týdnu
                activity.date = format_date(activity.date, format='EEEE d. MMMM', locale='cs_CZ')
                other_activities.append({'activity': activity})

        context = {
            'todays_activities': todays_activities,
            'other_activities': other_activities
        }

    else:
        context = {'no_activities': True}

    return render(request, 'day_schedule.html', context)
