from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prihlaseni', views.login_user, name='login_user'),
    path('help', views.help_w_registration, name='help'),
    path('odhlaseni', views.logout_user, name='logout_user'),
    path('registrace', views.register_user, name='registration'),
]
