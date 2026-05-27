from django.conf import settings
from django.core.mail import send_mail
from taxi.services.messaging import send_sms, send_whatsapp


def send_booking_created_notification(reservation):
    """
    Called when reservation is created (pending/cash booking)
    """

    message = f"""
    🚖 New Booking Created

    Name: {reservation.first_name} {reservation.last_name}
    Pickup: {reservation.pickup_location}
    Dropoff: {reservation.dropoff_location}
    Date: {reservation.pickup_date}
    Time: {reservation.pickup_time}
    Vehicle: {reservation.vehicle}

    Status: {reservation.payment_status}
    """

    # WhatsApp admin alert
    send_whatsapp(message, settings.TWILIO_WHATSAPP)

    # SMS to all admins
    for phone in settings.ADMIN_PHONES:
        send_sms(message, phone)

    # Email admin
    send_mail(
        subject="New Booking Created",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=settings.ADMIN_EMAIL,
        fail_silently=True,
    )


def send_payment_success_notification(reservation):
    """
    Called after Stripe/PayPal success
    """

    message = f"""
    ✅ Payment Successful

    Booking: {reservation.confirmation_number}
    Customer: {reservation.first_name} {reservation.last_name}
    Amount Paid: {reservation.vehicle.price if reservation.vehicle else 'N/A'}
    """

    send_whatsapp(message, settings.TWILIO_WHATSAPP)

    for phone in settings.ADMIN_PHONES:
        send_sms(message, phone)


def send_customer_confirmation_email(reservation):
    """
    Optional: email customer after booking
    """
    send_mail(
        subject="Your Reservation is Confirmed",
        message=f"Hi {reservation.first_name}, your booking is confirmed.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reservation.email],
        fail_silently=True,
    )