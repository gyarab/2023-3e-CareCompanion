from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_login'),
    path('/help', views.help_w_registration, name='help'),
]
