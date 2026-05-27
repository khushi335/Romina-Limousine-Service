from django.contrib import admin
from .models import ContactMessage, Reservation, Vehicle

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "confirmation_number",
        "first_name",
        "pickup_date",
        "vehicle",
        "payment_status",
        "created_at",
    )

    list_filter = ("payment_status", "pickup_date", "vehicle")
    search_fields = ("first_name", "email", "phone_number")
    readonly_fields = ("confirmation_number", "created_at")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "passengers", "luggage")
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('created_at',)

