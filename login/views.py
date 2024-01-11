from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterUserForm


def index(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        # TODO: osetrit presmerovani po loginu
        if user is not None:
            login(request, user)
            return redirect("/opatrovnik")
        else:
            messages.success(request,
                             'Při přihlašování nastala chyba, znova si zkontrolujte zadané údaje, případně se obraťte na IT podporu. ')
            return redirect("/prihlaseni")


    else:
        return render(request, 'index_login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně')
    return redirect('index_login')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registrace proběhla úspěšně')
            return redirect('/opatrovnik')

    else:
        form = RegisterUserForm()

    return render(request, 'register.html', {'form': form})


def help_w_registration(request):
    return render(request, 'help.html')
