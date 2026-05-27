from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def create_event(reservation):
    creds = Credentials.from_service_account_file("google_credentials.json")

    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": "Luxury Booking",
        "description": f"{reservation.first_name} {reservation.last_name}",
        "start": {
            "dateTime": f"{reservation.pickup_date}T{reservation.pickup_time}",
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": f"{reservation.pickup_date}T{reservation.pickup_time}",
            "timeZone": "UTC",
        },
    }

    service.events().insert(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        body=event
    ).execute()