from django.shortcuts import render

from .decorators import patient_required


@patient_required
def index(request):
    return render(request, 'index_patient.html')


@patient_required
def caregivers_list(request):
    return render(request, 'caregivers_list.html')


@patient_required
def contacts(request):
    return render(request, 'contacts.html')


@patient_required
def day_schedule(request):
    return render(request, 'day_schedule.html')
