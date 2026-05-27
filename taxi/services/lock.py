from django.core.cache import cache
from taxi.models import Reservation

LOCK_SECONDS = 300  # 5 min lock

def generate_lock_key(vehicle_id, date, time):
    return f"lock:{vehicle_id}:{date}:{time}"


def lock_slot(vehicle_id, date, time):
    key = generate_lock_key(vehicle_id, date, time)
    if cache.get(key):
        return False
    cache.set(key, "locked", LOCK_SECONDS)
    return True


def release_slot(vehicle_id, date, time):
    cache.delete(generate_lock_key(vehicle_id, date, time))


def is_slot_taken(vehicle, date, time):
    return Reservation.objects.filter(
        vehicle=vehicle,
        pickup_date=date,
        pickup_time=time
    ).exists()