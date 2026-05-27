from django.db import models
from django.core.exceptions import ValidationError
import uuid
from datetime import date, time


# -------------------------
# CONTACT FORM
# -------------------------
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


# -------------------------
# VEHICLE MODEL
# -------------------------
class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    passengers = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="vehicles/")

    def __str__(self):
        return self.name


# -------------------------
# RESERVATION MODEL (CORE FIXED)
# -------------------------
class Reservation(models.Model):

    # PAYMENT TYPES
    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card (Stripe)"),
        ("paypal", "PayPal"),
    ]

    # STATUS
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    # UNIQUE ID
    confirmation_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # -------------------------
    # TRIP INFO
    # -------------------------
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)

    pickup_date = models.DateField()
    pickup_time = models.TimeField()

    passengers = models.PositiveIntegerField()

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # -------------------------
    # CUSTOMER INFO
    # -------------------------
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    # -------------------------
    # PAYMENT INFO
    # -------------------------
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    payment_status = models.CharField(
        max_length=50,
        default="unpaid"
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # -------------------------
    # SYSTEM
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["pickup_date", "pickup_time"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.confirmation_number}"

    # -------------------------
    # CLEAN VALIDATION (IMPORTANT FIX)
    # -------------------------
    def clean(self):
        from django.utils import timezone
        if self.pickup_date and self.pickup_date < timezone.now().date():
            raise ValidationError({"pickup_date": "Pickup date cannot be in the past."})

    # -------------------------
    # HELPER METHODS (USED IN TEMPLATE FIX)
    # -------------------------
    def vehicle_name(self):
        return self.vehicle.name if self.vehicle else ""

    def vehicle_luggage(self):
        return self.vehicle.luggage if self.vehicle else 0