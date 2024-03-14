from django.shortcuts import render

from caregiver.models import Caregiver
from .decorators import patient_required
from datetime import datetime, time, date, timezone


@patient_required
def index(request):
    return render(request, 'index_patient.html')


@patient_required
def caregivers_list(request):
    now = datetime.now()

    users_shift_info = []
    for caregiver in Caregiver.objects.prefetch_related('shift_set'):
        shifts_today = caregiver.shift_set.filter(date_of_shift=now.date())
        if shifts_today.exists():
            shift = shifts_today.first()
            shift_start = datetime.combine(now.date(), shift.start)
            shift_end = datetime.combine(now.date(), shift.end)
            on_shift = shift_start <= now <= shift_end
            users_shift_info.append({
                'first_name': caregiver.first_name,
                'last_name': caregiver.surname,
                'on_shift': on_shift,
                'shift_end': shift.end if on_shift else None,
            })
        else:
            next_shift = caregiver.shift_set.filter(date_of_shift__gt=now.date()).order_by('date_of_shift',
                                                                                           'start').first()
            if next_shift is not None:  # Check if next_shift is not None
                users_shift_info.append({
                    'first_name': caregiver.first_name,
                    'last_name': caregiver.surname,
                    'on_shift': False,
                    'next_shift_date': next_shift.date_of_shift,
                    'next_shift_start': next_shift.start,
                })
            else:
                users_shift_info.append({
                    'first_name': caregiver.first_name,
                    'last_name': caregiver.surname,
                    'on_shift': False,
                    'next_shift_date': 'no upcoming shifts',
                    'next_shift_start': '',
                })

    return render(request, 'caregivers_list.html', {'users_shift_info': users_shift_info})


@patient_required
def contacts(request):
    patient = request.user.patient_profile
    return render(request, 'contacts.html', {'patient': patient})


@patient_required
def day_schedule(request):
    return render(request, 'day_schedule.html')
