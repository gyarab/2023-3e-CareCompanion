from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prihlaseni/', views.login_user, name='login_user'),
    path('sprava/', views.administration, name='administration'),
    path('sprava/vytvoreni-uctu/', views.account_creation, name='account_creation'),
    path('sprava/registrace-klienta/', views.register_patient, name='patient_registration'),
    # path('sprava/registrace-opatrovnika/', views.register_caregiver, name='caregiver_registration'),
    # path('sprava/smeny/', views.register_caregiver, name='caregiver_registration'),
    # path('sprava/smeny/<str:full_name_of_caregiver>/', views.register_caregiver, name='caregiver_registration'),
    path('sprava/uzivatele/', views.display_users, name='display_users'),
    path('sprava/uzivatele/<str:info_on_user>/', views.user_update, name='user_update'),
    path('sprava/uzivatele/<str:info_on_user>/zmena-infa/', views.patient_update, name='patient_update'),
    path('sprava/uzivatele/<str:info_on_user>/zmena-hesla/', views.user_reset_password, name='user_reset_password'),
    path('odhlaseni/', views.logout_user, name='logout_user'),
]
