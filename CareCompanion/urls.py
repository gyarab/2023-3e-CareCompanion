from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('opatrovnik', include('caretaker.urls')),
    path('klient', include('patient.urls')),
    path('prihlaseni', include('login.urls')),
    path('prihlaseni', include('django.contrib.auth.urls')),
]
