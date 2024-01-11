from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('opatrovnik', include('caregiver.urls')),
    path('klient', include('patient.urls')),
    path('', include('home.urls')),
    path('', include('django.contrib.auth.urls')),
]
