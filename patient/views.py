from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index_patient.html')


def caregivers_list(request):
    return render(request, 'caregivers_list.html')


def contacts(request):
    return render(request, 'contacts.html')


def day_schedule(request):
    return render(request, 'day_schedule.html')
