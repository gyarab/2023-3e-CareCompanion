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
    caregiver = request.user.caregiver_profile
    context = {'caregiver': caregiver}
    now = datetime.now()

    # Saves the first upcoming/current shift (either today or in the future)
    shifts = caregiver.shift_set.filter(
        Q(date_of_shift__gt=now.date()) |  # Future shifts OR
        (Q(date_of_shift=now.date()) & Q(end__gt=now.time()))  # Today's shifts that have not ended
    ).order_by('date_of_shift', 'start')

    if shifts:
        context.update({'shifts': shifts})
        soonest_shift = shifts.first()
        shift_start = datetime.combine(soonest_shift.date_of_shift, soonest_shift.start)
        shift_end = datetime.combine(soonest_shift.date_of_shift, soonest_shift.end)

        # smeny dnes (probihaji nebo jeste budou)
        if shift_start <= now <= shift_end or soonest_shift.date_of_shift == now.date():
            context = {
                'today': True,
                'shift_start': shift_start.time,
                'shift_end': shift_end.time,
                'activities': soonest_shift.activity_set.all
            }
            shifts = shifts[1:]

        # nadchazejici smeny
        if shifts:
            upcoming_shifts_info = []
            for upcoming_shift in shifts:
                upcoming_shifts_info.append({
                    'upcom_shift_date': format_date(upcoming_shift.date_of_shift, format='EEEE d. MMMM', locale='cs_CZ'),
                    'upcom_shift_start': upcoming_shift.start,
                    'upcom_shift_end': upcoming_shift.end,
                    'activities': upcoming_shift.activity_set.all
                })

            context.update({'upcoming_shifts_info': upcoming_shifts_info})

        else:
            context.update({'shifts': shifts})

        # next_shift_date = format_date(soonest_shift.date_of_shift, format='EEEE d. MMMM', locale='cs_CZ')
        # context = {
        #     'caregiver': caregiver,
        #     'on_shift': False,
        #     'shift_date': next_shift_date,
        #     'shift_start': soonest_shift.start,
        #     'shift_end': soonest_shift.end,
        #     'today': soonest_shift.date_of_shift == now.date(),
        #     'activities': soonest_shift.activity_set.all
        # }
    else:
        context.update({'shifts': shifts})

    return render(request, 'shift_schedule.html', context)


@caregiver_required
def floor_map(request):
    patients = Patient.objects.all()
    return render(request, 'floor_map.html', {'patients': patients})


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
