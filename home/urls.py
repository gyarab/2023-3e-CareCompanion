from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prihlaseni/', views.login_user, name='login_user'),
    path('sprava/', views.administration, name='administration'),
    path('sprava/vytvoreni-uctu/', views.account_creation, name='account_creation'),
    path('sprava/registrace-klienta/', views.register_patient, name='patient_registration'),
    path('sprava/registrace-opatrovnika/', views.register_caregiver, name='caregiver_registration'),
    path('odhlaseni/', views.logout_user, name='logout_user'),
]
