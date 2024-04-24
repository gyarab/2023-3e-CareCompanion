from django.urls import path

from . import views

urlpatterns = [
    # Homepage aplikace
    path('', views.index, name='index'),
    # Přihlášení uživatele
    path('prihlaseni/', views.login_user, name='login_user'),
    # Home administrátora
    path('sprava/', views.administration, name='administration'),
    # Tvorba uživatelských účtů
    path('sprava/vytvoreni-uctu/', views.account_creation, name='account_creation'),
    # Tvorba profilu pro klienta
    path('sprava/registrace-klienta/', views.universal_patient_form, name='patient_registration'),
    # Směny opatrovníků
    path('sprava/smeny/', views.shifts, name='shifts'),
    # Úprava směn konkrétního opatrovníka
    path('sprava/smeny/<int:pk>/', views.edit_shifts, name='edit_shifts'),
    # Rozvrhy klientů
    path('sprava/aktivity/', views.patient_activities, name='patient_activities'),
    # Úprava rozvrhů konkrétního klienta
    path('sprava/aktivity/<int:pk>/', views.edit_patient_activities, name='edit_patient_activities'),
    # Všechny uživatelské účty
    path('sprava/uzivatele/', views.display_users, name='display_users'),
    # Zobrazení a úprava infa o konkrétním uživatelském účtu
    path('sprava/uzivatele/<str:info_on_user>/', views.user_update, name='user_update'),
    # Změna klientských informací konkrétního klienta
    path('sprava/uzivatele/<str:info_on_user>/zmena-infa/', views.universal_patient_form, name='patient_update'),
    # Změna hesla konkrétního uživatele
    path('sprava/uzivatele/<str:info_on_user>/zmena-hesla/', views.user_reset_password, name='user_reset_password'),
    # Smazání konkrétního uživatele
    path('sprava/uzivatele/smazat-<int:pk>/', views.delete_user, name='delete_user'),
    # Odhlášení
    path('odhlaseni/', views.logout_user, name='logout_user')
]
