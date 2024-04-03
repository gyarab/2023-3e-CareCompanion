from datetime import datetime
from babel.dates import format_date

from django.db.models import Q
from django.shortcuts import render

from .decorators import caregiver_required
from patient.models import Patient


@caregiver_required
def index(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    return render(request, 'index_caregiver.html', {'first_name': first_name,
                                                    'last_name': last_name})


@caregiver_required
def medical_cards(request):
    patients = Patient.objects.all()
    return render(request, 'medical_cards.html', {'patients': patients})


@caregiver_required
def patient_info(request, full_name_of_patient):
    first_name, last_name = full_name_of_patient.split('-')
    patient = Patient.objects.get(user__first_name=first_name, user__last_name=last_name)
    return render(request, 'patient_info.html', {'patient': patient})


@caregiver_required
def shift_schedule(request):
    # caregivers = Caregiver.objects.all()
    caregiver = request.user.caregiver_profile
    now = datetime.now()

    # Saves the first upcoming/current shift (either today or in the future)
    next_shift = caregiver.shift_set.filter(
        Q(date_of_shift__gt=now.date()) |  # Future shifts OR
        (Q(date_of_shift=now.date()) & Q(end__gt=now.time()))  # Today's shifts that have not ended
    ).order_by('date_of_shift', 'start').first()

    if next_shift:
        shift_start = datetime.combine(next_shift.date_of_shift, next_shift.start)
        shift_end = datetime.combine(next_shift.date_of_shift, next_shift.end)
        if shift_start <= now <= shift_end:

            # If the shift has already started but not ended, the caregiver is on shift
            context = {
                'caregiver': caregiver,
                'on_shift': True,
                'shift_start': shift_start.time,
                'shift_end': shift_end.time,
                'activities':  next_shift.activity_set.all
            }
        else:
            # If the shift is upcoming, displaying its details
            next_shift_date = format_date(next_shift.date_of_shift, format='EEEE d. MMMM', locale='cs_CZ')
            context = {
                'caregiver': caregiver,
                'on_shift': False,
                'next_shift_date': next_shift_date,
                'next_shift_start': next_shift.start,
                'activities': next_shift.activity_set.all
            }
    else:
        context = {
            'caregiver': caregiver,
            'on_shift': False,
            'next_shift_date': False
        }

    context.update({})
    return render(request, 'shift_schedule.html', context)


@caregiver_required
def floor_map(request):
    return render(request, 'floor_map.html')


@caregiver_required
def manual(request):
    return render(request, 'manual.html')


@caregiver_required
def what_to_do(request):
    return render(request, 'what_to_do.html')


@caregiver_required
def activities(request):
    return render(request, 'activities.html')


@caregiver_required
def education(request):
    return render(request, 'education.html')
