from django.db import transaction
from django.contrib import messages

from .models import Reservation
from .services.lock import is_slot_taken
from .tasks import send_booking_notifications
from .services.calendar import create_event


def _finalize_reservation(
    request,
    data,
    payment_status="pending",
    transaction_id=None
):
    vehicle = data["vehicle"]
    pickup_date = data["pickup_date"]
    pickup_time = data["pickup_time"]

    # prevent duplicate booking for same vehicle/date/time
    if is_slot_taken(vehicle, pickup_date, pickup_time):
        messages.error(
            request,
            "This slot is already booked. Please choose another time."
        )
        return None

    with transaction.atomic():
        reservation = Reservation.objects.create(
            pickup_location=data["pickup_location"],
            dropoff_location=data["dropoff_location"],
            pickup_date=pickup_date,
            pickup_time=pickup_time,
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

    # celery
    try:
        send_booking_notifications.delay(reservation.id)
    except Exception as e:
        print("Celery error:", e)

    # google calendar
    try:
        create_event(reservation)
    except Exception as e:
        print("Calendar error:", e)

    return reservation