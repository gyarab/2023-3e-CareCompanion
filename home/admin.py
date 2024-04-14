from django.contrib import admin
from .models import Contact, Address, DaySchedule, Announcement


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'zip_code', 'city')


@admin.register(DaySchedule)
class DayScheduleAdmin(admin.ModelAdmin):
    list_display = ('time', 'description')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('text', 'delete_date', 'delete_time')
