from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index_caretaker.html')


def medical_cards(request):
    return render(request, 'medical_cards.html')


def shift_schedule(request):
    return render(request, 'shift_schedule.html')


def floor_map(request):
    return render(request, 'floor_map.html')


def manual(request):
    return render(request, 'manual.html')
