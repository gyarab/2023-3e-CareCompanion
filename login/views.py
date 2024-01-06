from django.shortcuts import render


def index(request):
    return render(request, 'index_login.html')


def help_w_registration(request):
    return render(request, 'help.html')
