from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Caregiver, Shift, Activity


class ActivityInline(NestedStackedInline):
    model = Activity
    extra = 0


class ShiftInline(NestedStackedInline):
    model = Shift
    extra = 0
    inlines = [ActivityInline]


class CaregiverAdmin(NestedModelAdmin):
    inlines = [ShiftInline]
    list_display = ('first_name', 'last_name')


admin.site.register(Caregiver, CaregiverAdmin)
