from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from .models import ContactMessage, Reservation, Vehicle
from django.urls import reverse
from urllib.parse import urlencode
import uuid
from datetime import date, time
from .forms import Step1Form, Step3Form
from .utils import _finalize_reservation
from .services.payment import create_checkout_session
from .utils import send_whatsapp_message

def index(request):
    admin_recipient = getattr(settings, 'ADMIN_EMAIL', ['sahkhushi946@gmail.com'])

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Logic: Initial 'if' for the first form type
        if form_type == 'contact_form':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject', 'General Inquiry')
            message_body = request.POST.get('message')

            ContactMessage.objects.create(
                full_name=name, email=email, phone=phone,
                subject=subject, message=message_body
            )

            context = {
                'name': name, 'email': email, 'phone': phone, 
                'subject': subject, 'message': message_body,'inquiry_date': datetime.now().strftime("%B %d, %Y")
            }
            
            admin_html = render_to_string('emails/admin_new_contact.html', context)
            admin_msg = EmailMultiAlternatives(
                f"New Inquiry: {subject}", 
                strip_tags(admin_html), 
                settings.DEFAULT_FROM_EMAIL, 
                admin_recipient
            )
            admin_msg.attach_alternative(admin_html, "text/html")
            admin_msg.send(fail_silently=False)

            cust_html = render_to_string('emails/customer_reply.html', context)
            cust_msg = EmailMultiAlternatives(
                "Message Received - Romina Limousine Service", 
                strip_tags(cust_html), 
                settings.DEFAULT_FROM_EMAIL, 
                [email]
            )
            cust_msg.attach_alternative(cust_html, "text/html")
            cust_msg.send(fail_silently=False)

            messages.success(request, "Your message has been sent. Thank you!")
            return redirect('/#contact-card')

    return render(request, 'taxi/index.html')

def make_reservation(request):
    step = int(request.GET.get("step", 1))

    # =========================
    # STEP 1
    # =========================
    if step == 1:
        form = Step1Form(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                data = form.cleaned_data.copy()

                # convert date/time for session
                data["pickup_date"] = data["pickup_date"].isoformat()
                data["pickup_time"] = data["pickup_time"].isoformat()

                request.session["step1"] = data

                return redirect("/reservation/?step=2")

            else:
                print(form.errors)

        return render(
            request,
            "taxi/reservation.html",
            {
                "current_step": 1,
                "form": form,
            },
        )

    # =========================
    # STEP 2
    # =========================
    elif step == 2:
        vehicles = Vehicle.objects.all()

        if request.method == "POST":
            vehicle_id = request.POST.get("selected_vehicle_id")

            if not vehicle_id:
                messages.error(
                    request,
                    "Please select a vehicle."
                )
                return redirect("/reservation/?step=2")

            request.session["vehicle_id"] = vehicle_id

            return redirect("/reservation/?step=3")

        return render(
            request,
            "taxi/reservation.html",
            {
                "current_step": 2,
                "vehicles": vehicles,
            },
        )

    # =========================
    # STEP 3
    # =========================
    elif step == 3:
        form = Step3Form(request.POST or None)

        if request.method == "POST":
            if form.is_valid():

                step1_raw = request.session.get("step1")

                if not step1_raw:
                    messages.error(
                        request,
                        "Session expired. Please start again."
                    )
                    return redirect("/reservation/?step=1")

                # convert session strings back
                step1 = step1_raw.copy()

                step1["pickup_date"] = date.fromisoformat(
                    step1["pickup_date"]
                )

                step1["pickup_time"] = time.fromisoformat(
                    step1["pickup_time"]
                )

                vehicle = get_object_or_404(
                    Vehicle,
                    id=request.session.get("vehicle_id")
                )

                data = {
                    **step1,
                    **form.cleaned_data,
                    "vehicle": vehicle,
                }

                reservation = _finalize_reservation(
                    request,
                    data,
                    payment_status="pending"
                )

                # slot already taken
                if reservation is None:
                    return render(
                        request,
                        "taxi/reservation.html",
                        {
                            "current_step": 3,
                            "form": form,
                        },
                    )

                # =========================
                # SEND WHATSAPP
                # =========================
                message = (
                    f"🚖 New Reservation\n\n"
                    f"Name: {reservation.first_name}\n"
                    f"Date: {reservation.pickup_date}\n"
                    f"Time: {reservation.pickup_time}\n"
                    f"Pickup: {reservation.pickup_location}\n"
                    f"Dropoff: {reservation.dropoff_location}\n"
                    f"Vehicle: {reservation.vehicle}\n"
                    f"Phone: {reservation.phone_number}"
                )

                send_whatsapp_message(
                    "+9779821837931",
                    message
                )

                return redirect(
                    "booking_confirmation",
                    reservation.confirmation_number
                )

            else:
                print(form.errors)

        return render(
            request,
            "taxi/reservation.html",
            {
                "current_step": 3,
                "form": form,
            },
        )

    # =========================
    # fallback
    # =========================
    return redirect("/reservation/?step=1")

# -------------------
# STRIPE SUCCESS
# -------------------
def stripe_success(request):
    step1 = request.session.get("step1")
    vehicle = get_object_or_404(Vehicle, id=request.session.get("vehicle_id"))

    data = {
        **step1,
        "vehicle": vehicle
    }

    reservation = _finalize_reservation(
        request,
        data,
        payment_status="paid",
        transaction_id="stripe"
    )

    return redirect("booking_confirmation", reservation.confirmation_number)


# -------------------
# BOOKING CONFIRMATION
# -------------------
def booking_confirmation(request, confirmation_number):
    reservation = get_object_or_404(Reservation, confirmation_number=confirmation_number)

    return render(request, "taxi/booking_confirmation.html", {
        "reservation": reservation
    })

# -------------------
# PAYPAL
# -------------------
def paypal_process(request):
    data = {
        **request.session.get("step1", {}),
    }

    amount = data.get("price", 0)
    invoice_id = str(uuid.uuid4())

    params = {
        "cmd": "_xclick",
        "business": settings.PAYPAL_PERSONAL_EMAIL,
        "item_name": "Limousine Booking",
        "item_number": invoice_id,
        "amount": amount,
        "currency_code": "USD",
        "return": request.build_absolute_uri(reverse("paypal_return")),
        "cancel_return": request.build_absolute_uri(reverse("paypal_cancel")),
    }

    return redirect(f"{settings.PAYPAL_URL}?{urlencode(params)}")


def paypal_return(request):
    step1 = request.session.get("step1")
    vehicle = get_object_or_404(Vehicle, id=request.session.get("vehicle_id"))

    data = {
        **step1,
        "vehicle": vehicle
    }

    reservation = _finalize_reservation(
        request,
        data,
        payment_status="paypal_paid",
        transaction_id=request.GET.get("tx")
    )

    return redirect("booking_confirmation", reservation.confirmation_number)


def paypal_cancel(request):
    messages.error(request, "Payment cancelled.")
    return redirect("make_reservation")
    
def cities_served(request):
    context = {
        'maryland_cities': [
            'Baltimore', 'Annapolis', 'Columbia', 'Frederick', 'Rockville', 
            'Gaithersburg', 'Bethesda', 'Silver Spring', 'Towson', 'Bowie', 
            'Ellicott City', 'Easton', 'Hagerstown', 'Ocean City', 'Salisbury', 
            'Laurel', 'Greenbelt', 'College Park'
        ],
        'dc_neighborhoods': [
            'Downtown DC', 'Capitol Hill', 'Georgetown', 'Dupont Circle', 
            'Foggy Bottom', 'Adams Morgan', 'Navy Yard', 'NoMa'
        ],
        'virginia_cities': [
            'Arlington', 'Alexandria', 'McLean', 'Tysons Corner', 
            'Reston', 'Herndon', 'Fairfax', 'Springfield'
        ]
    }
    return render(request, 'taxi/cities.html', context)
    
def contact(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        project = request.POST.get('project', 'General Inquiry')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        # 1. Save to Database
        ContactMessage.objects.create(
            full_name=name, email=email, phone=phone,
            subject=subject, message=message_body
        )

        context = {
            'name': name, 'email': email, 'phone': phone, 
            'project': project, 'subject': subject, 'message': message_body,'inquiry_date': datetime.now().strftime("%B %d, %Y")
        }

        # 2. Send Email to Admin(s)
        # settings.ADMIN_EMAIL is expected to be a list from your config
        admin_html = render_to_string('emails/admin_new_contact.html', context)
        admin_msg = EmailMultiAlternatives(
            f"New Inquiry: {subject}", 
            strip_tags(admin_html), 
            settings.DEFAULT_FROM_EMAIL, 
            settings.ADMIN_EMAIL 
        )
        admin_msg.attach_alternative(admin_html, "text/html")
        admin_msg.send(fail_silently=False)

        # 3. Send Confirmation Email to Customer
        cust_html = render_to_string('emails/customer_reply.html', context)
        cust_msg = EmailMultiAlternatives(
            "Message Received - Romina Limousine Service", 
            strip_tags(cust_html), 
            settings.DEFAULT_FROM_EMAIL, 
            [email]
        )
        cust_msg.attach_alternative(cust_html, "text/html")
        cust_msg.send(fail_silently=False)

        # 4. Success Feedback
        messages.success(request, "Your message has been sent successfully. Thank you for contacting Romina Limousine!")
        
        # Redirect back to the contact page
        return redirect('contact') 

    return render(request, 'taxi/contact.html')
    
def fleet(request):
    return render(request, 'taxi/fleet.html')
    
def service(request):
    return render(request, 'taxi/service.html')
    
def our_rate(request):
    return render(request, 'taxi/rate.html')