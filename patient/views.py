from django.shortcuts import render
from django.db.models import Q, ExpressionWrapper, BooleanField, F
from babel.dates import format_date

from caregiver.models import Caregiver
from home.decorators import patient_required
from datetime import datetime


@patient_required
def index(request):
    date = format_date(datetime.now(), format='EEEE d. MMMM', locale='cs_CZ')
    return render(request, 'index_patient.html', {'date': date})


@patient_required
def caregivers_list(request):
    now = datetime.now()
    caregivers_shift_info = []

    for caregiver in Caregiver.objects.prefetch_related('shift_set').order_by('user__last_name'):

        next_shift = caregiver.shift_set.annotate(
                is_overnight=ExpressionWrapper(
                    Q(end__lt=F('start')),
                    output_field=BooleanField()
                )
            ).filter(
                Q(date_of_shift__gt=now.date()) |
                (Q(date_of_shift=now.date()) & (Q(end__gt=now.time()) | Q(is_overnight=True)))
            ).order_by('date_of_shift', 'start').first()

        if next_shift:
            shift_start = datetime.combine(next_shift.date_of_shift, next_shift.start)
            shift_end = datetime.combine(next_shift.date_of_shift, next_shift.end)

            if shift_start <= now <= shift_end or (next_shift.is_overnight_shift() and shift_start <= now):
                caregivers_shift_info.append({
                    'first_name': caregiver.first_name,
                    'last_name': caregiver.last_name,
                    'on_shift': True,
                    'shift_end': next_shift.end,
                })
            else:
                next_shift_date = format_date(next_shift.date_of_shift, format='EEEE d. MMMM', locale='cs_CZ')
                caregivers_shift_info.append({
                    'first_name': caregiver.first_name,
                    'last_name': caregiver.last_name,
                    'on_shift': False,
                    'next_shift_date': next_shift_date,
                    'next_shift_start': next_shift.start,
                    'next_shift_end': next_shift.end
                })
        else:
            caregivers_shift_info.append({
                'first_name': caregiver.first_name,
                'last_name': caregiver.last_name,
                'on_shift': False,
                'no_upc_shifts': True
            })

    context = {'caregivers_shift_info': caregivers_shift_info}

    return render(request, 'caregivers_list.html', context)


@patient_required
def contacts(request):
    patient = request.user.patient_profile
    return render(request, 'contacts.html', {'patient': patient})


@patient_required
def day_schedule(request):
    patient = request.user.patient_profile
    now = datetime.now()
    activities = patient.activity_set.filter(date__gte=now.date())

    if activities:
        todays_activities = []
        other_activities = []

        for activity in activities:
            if activity.date == now.date():
                todays_activities.append({'activity': activity})
            else:
                activity.date = format_date(activity.date, format='EEEE d. MMMM', locale='cs_CZ')
                other_activities.append({'activity': activity})

        context = {
            'todays_activities': todays_activities,
            'other_activities': other_activities
        }

    else:
        context = {'no_activities': True}

    return render(request, 'day_schedule.html', context)
