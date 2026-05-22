from django.db import models

class Booking(models.Model):
    # Required Fields
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_date = models.DateField()
    pickup_time = models.CharField(max_length=20) # Storing as string to keep HH:MM AM/PM format
    pickup_address = models.TextField()
    dropoff_location = models.TextField()
    
    # Optional Fields
    company = models.CharField(max_length=100, blank=True, null=True)
    special_notes = models.TextField(blank=True, null=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_date}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        
        
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.full_name}"
        
        
class Reservation(models.Model):
    name = models.CharField(max_length=100)
    date_of_service = models.DateField()
    pickup_time = models.CharField(max_length=20) # Stores HH:MM AM/PM
    pickup_address = models.TextField()
    dropoff_location = models.TextField()
    email = models.EmailField()
    mobile_contact = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    special_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date_of_service}"