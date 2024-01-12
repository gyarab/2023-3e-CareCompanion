from django.shortcuts import render

from .decorators import caregiver_required


@caregiver_required
def index(request):
    return render(request, 'index_caregiver.html')


@caregiver_required
def medical_cards(request):
    return render(request, 'medical_cards.html')


@caregiver_required
def shift_schedule(request):
    return render(request, 'shift_schedule.html')


@caregiver_required
def floor_map(request):
    return render(request, 'floor_map.html')


@caregiver_required
def manual(request):
    return render(request, 'manual.html')
