from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from taxi.services.messaging import send_whatsapp, send_sms
from taxi.models import Reservation


@shared_task
def send_booking_notifications(reservation_id):

    try:
        reservation = Reservation.objects.get(id=reservation_id)

        msg = f"""
🚖 NEW BOOKING CONFIRMED

Name: {reservation.first_name} {reservation.last_name}
Pickup: {reservation.pickup_location}
Dropoff: {reservation.dropoff_location}
Date: {reservation.pickup_date}
Time: {reservation.pickup_time}
Vehicle: {reservation.vehicle.name if reservation.vehicle else "N/A"}
Status: CONFIRMED
"""

        send_whatsapp(msg, settings.TWILIO_WHATSAPP)

        for phone in settings.ADMIN_PHONES:
            send_sms(msg, phone)

        send_mail(
            subject="🚖 New Booking Confirmed",
            message=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ADMIN_EMAIL,
            fail_silently=True
        )

        return "Notification sent successfully"

    except Reservation.DoesNotExist:
        return "Reservation not found"

    except Exception as e:
        return f"Notification failed: {str(e)}"