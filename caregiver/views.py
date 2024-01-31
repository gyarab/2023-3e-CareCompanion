from django.shortcuts import render

from .decorators import caregiver_required
from caregiver.models import Caregiver
from patient.models import Patient


@caregiver_required
def index(request):
    first_name = request.user.caregiver_profile.first_name
    surname = request.user.caregiver_profile.surname
    return render(request, 'index_caregiver.html', {'first_name': first_name,
                                                    'surname': surname})


@caregiver_required
def medical_cards(request):
    patients = Patient.objects.all()
    return render(request, 'medical_cards.html', {'patients': patients})


@caregiver_required
def patient_info(request, full_name_of_patient):
    first_name, surname = full_name_of_patient.split('-')
    patient = Patient.objects.get(first_name=first_name, surname=surname)
    return render(request, 'patient_info.html', {'patient': patient})


@caregiver_required
def shift_schedule(request):
    # caregivers = Caregiver.objects.all()
    caregiver = request.user.caregiver_profile
    return render(request, 'shift_schedule.html', {'caregiver': caregiver})


@caregiver_required
def floor_map(request):
    return render(request, 'floor_map.html')


@caregiver_required
def manual(request):
    return render(request, 'manual.html')
