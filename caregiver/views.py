from datetime import datetime

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
    current_date_time = datetime.now()
    month = datetime.today().month
    day = datetime.today().day
    year = datetime.today().year
    time = datetime.now().time()

    context = {
        'caregiver': caregiver,
        'current_month': month,
        'current_day': day,
        'current_year': year,
        'current_time': time,
        'current_date_time': current_date_time
    }
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
