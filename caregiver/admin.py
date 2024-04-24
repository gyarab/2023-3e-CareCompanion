from django.contrib import admin

from .models import Caregiver, Shift


# Postará se o to jak se modely Shift a Caregiver zobrazí na django-admin stránce

class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 0


class CaregiverAdmin(admin.ModelAdmin):
    inlines = [ShiftInline]
    list_display = ('first_name', 'last_name')


admin.site.register(Caregiver, CaregiverAdmin)
