from django.contrib import admin
from .models import Booking, ContactMessage, Reservation

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service_date', 'pickup_time', 'phone', 'created_at')
    list_filter = ('service_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'pickup_address')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('full_name', 'email', 'phone', 'company')
        }),
        ('Trip Details', {
            'fields': ('service_date', 'pickup_time', 'pickup_address', 'dropoff_location')
        }),
        ('Additional Info', {
            'fields': ('special_notes', 'created_at')
        }),
    )
    
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('created_at',)
    
    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_service', 'pickup_time', 'email', 'mobile_contact')
    list_filter = ('date_of_service',)
    search_fields = ('name', 'email', 'pickup_address')
    readonly_fields = ('created_at',)