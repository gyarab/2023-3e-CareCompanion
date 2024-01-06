from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
            messages.success(request, 'Při přihlašování nastala chyba, znova si zkontrolujte zadané údaje, případně se obraťte na IT podporu. ')
            return redirect("/prihlaseni")


    else:
        return render(request, 'index_login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Odhlášení proběhlo úspěšně')
    return redirect('index_login')


def help_w_registration(request):
    return render(request, 'help.html')
