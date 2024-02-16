from datetime import date

from django.shortcuts import render

from caregiver.models import Caregiver
from .decorators import patient_required


@patient_required
def index(request):
    return render(request, 'index_patient.html')


@patient_required
def caregivers_list(request):
    # display list of all caregivers that have shift today and the end time of the shift
    today = date.today()

    # Retrieve caregivers with shifts for today
    caregivers = Caregiver.objects.filter(shift__date_of_shift=today).select_related('user')
    users_last_shift_info = []
    for caregiver in caregivers:
        last_shift_date = caregiver.shift_set.order_by('-date_of_shift').first()
        if last_shift_date:
            users_last_shift_info.append({
                'first_name': caregiver.first_name,
                'last_name': caregiver.surname,
                'shift_date': last_shift_date.date_of_shift,
                'shift_end': last_shift_date.end
            })
    return render(request, 'caregivers_list.html', {'users_last_shift_info': users_last_shift_info})


@patient_required
def contacts(request):
    return render(request, 'contacts.html')


@patient_required
def day_schedule(request):
    return render(request, 'day_schedule.html')
