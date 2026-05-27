# messaging.py
import stripe
from twilio.rest import Client
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def send_whatsapp(message, to):
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP,
        body=message,
        to=to
    )


def send_sms(message, phone):
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_WHATSAPP,  # or SMS number if different
        to=phone
    )
    
    
