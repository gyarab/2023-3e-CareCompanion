from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .decorators import admin_required
from .forms import RegisterUserForm


def index(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Caregivers').exists():
                return redirect('index_caregiver')
            elif user.groups.filter(name='Patients').exists():
                return redirect('index_patient')
            else:
                return redirect('administration')

        else:
            messages.success(request,
                             'Při přihlašování nastala chyba, znova si zkontrolujte zadané údaje, případně se obraťte '
                             'na IT podporu. ')
            return redirect('login_user')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně')
    return redirect('index')


@admin_required
def administration(request):
    return render(request, 'administration.html')


@admin_required
def register_user(request):
    if request.method == 'POST':
        path = request.path
        if 'opatrovnika' in path:
            print('yur')
        else:
            pass
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrace proběhla úspěšně')
            return redirect('login_user')

    else:
        form = RegisterUserForm()

    return render(request, 'registration.html', {'form': form})


# @admin_required
# def register_user(request):
#     path = request.path
#     if request.method == 'POST':
#         if 'opatrovnik' in path:
#             form = RegistrationCaregiverForm(request.POST)
#         else:
#             form = RegistrationPatientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registrace proběhla úspěšně')
#             return redirect('login_user')
#
#     else:
#         if 'opatrovnik' in path:
#             form = RegistrationCaregiverForm()
#         else:
#             form = RegistrationPatientForm()
#
#     return render(request, 'registration.html', {'form': form,
#                                                  'caregiver': 'opatrovnik' in path})
