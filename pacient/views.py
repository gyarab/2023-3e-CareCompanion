from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index_pacient.html')


def caretakers_list(request):
    return render(request, 'caretakers_list.html')


def contacts(request):
    return render(request, 'contacts.html')


def schedule(request):
    return render(request, 'schedule.html')
