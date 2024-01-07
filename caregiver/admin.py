from django.contrib import admin
from .models import Caregiver, Shift


class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 1


class CaregiverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname')
    inlines = [ShiftInline]


admin.site.register(Caregiver, CaregiverAdmin)
