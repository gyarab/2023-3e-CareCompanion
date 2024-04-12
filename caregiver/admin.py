from django.contrib import admin

from .models import Caregiver, Shift


class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 0


class CaregiverAdmin(admin.ModelAdmin):
    inlines = [ShiftInline]
    list_display = ('first_name', 'last_name')


admin.site.register(Caregiver, CaregiverAdmin)
