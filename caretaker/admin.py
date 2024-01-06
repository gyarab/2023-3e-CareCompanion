from django.contrib import admin
from .models import Caretaker, Shift


class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 1


class CaretakerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname')
    inlines = [ShiftInline]


admin.site.register(Caretaker, CaretakerAdmin)
