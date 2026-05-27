from django.db import transaction
from .models import Reservation
from .services.lock import is_slot_taken
from .tasks import send_booking_notifications
from .services.calendar import create_event


def _finalize_reservation(request, data, payment_status="pending", transaction_id=None):

    vehicle = data["vehicle"]
    date = data["pickup_date"]
    time = data["pickup_time"]

    # 🚨 DOUBLE BOOKING PROTECTION
    if is_slot_taken(vehicle, date, time):
        raise Exception("This slot is already booked")

    with transaction.atomic():
        reservation = Reservation.objects.create(
            pickup_location=data["pickup_location"],
            dropoff_location=data["dropoff_location"],
            pickup_date=date,
            pickup_time=time,
            passengers=data["passengers"],
            vehicle=vehicle,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            payment_method=data["payment_method"],
            payment_status=payment_status,
            transaction_id=transaction_id,
        )

    # 🚀 ASYNC NOTIFICATION (BEST PRACTICE FIX)
    send_booking_notifications.delay(reservation.id)

    # 📅 GOOGLE CALENDAR
    try:
        create_event(reservation)
    except Exception as e:
        print(f"Calendar error: {e}")

    return reservation