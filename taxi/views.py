from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from .models import Booking, ContactMessage, Reservation

def index(request):
    # Get the admin email from settings, fallback if not found
    admin_recipient = getattr(settings, 'ADMIN_EMAIL', 'sahkhushi946@gmail.com')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # ---------------------------------------------------------
        # 1. LUXURY BOOKING FORM HANDLER
        # ---------------------------------------------------------
        if form_type == 'booking_form':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            raw_date = request.POST.get('service_date')
            time = request.POST.get('pickup_time')
            pickup = request.POST.get('pickup_address')
            dropoff = request.POST.get('dropoff_address')
            company = request.POST.get('company', '')
            notes = request.POST.get('notes', '')

            try:
                formatted_date = datetime.strptime(raw_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            except:
                formatted_date = raw_date 

            # Save to Database
            Booking.objects.create(
                full_name=name, email=email, phone=phone,
                service_date=formatted_date, pickup_time=time,
                pickup_address=pickup, dropoff_location=dropoff,
                company=company, special_notes=notes
            )

            # --- Emails for Booking ---
            admin_subject = f"🚨 NEW BOOKING: {name} - {formatted_date}"
            admin_body = f"Customer: {name}\nPhone: {phone}\nPick-up: {pickup}\nDrop-off: {dropoff}\nDate: {formatted_date} at {time}\nNotes: {notes}"
            
            # Send to Admin (sahkhushi946@gmail.com)
            send_mail(
                admin_subject, 
                admin_body, 
                settings.DEFAULT_FROM_EMAIL, 
                [admin_recipient], 
                fail_silently=False
            )

            # Send Confirmation to Customer
            send_mail(
                "Booking Received - Columbia Limozn", 
                f"Dear {name}, we received your booking for {formatted_date}. We will contact you shortly.", 
                settings.DEFAULT_FROM_EMAIL, 
                [email], 
                fail_silently=False
            )

            messages.success(request, "Your booking request was successful! Check your email for confirmation.")
            return redirect('index')

        # ---------------------------------------------------------
        # 2. CONTACT FORM HANDLER
        # ---------------------------------------------------------
        elif form_type == 'contact_form':
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
                'subject': subject, 'message': message_body
            }
            
            # Email to Admin (sahkhushi946@gmail.com)
            admin_html = render_to_string('emails/admin_new_contact.html', context)
            admin_msg = EmailMultiAlternatives(
                f"New Inquiry: {subject}", 
                strip_tags(admin_html), 
                settings.DEFAULT_FROM_EMAIL, 
                [admin_recipient] # Updated to use settings variable
            )
            admin_msg.attach_alternative(admin_html, "text/html")
            admin_msg.send(fail_silently=False)

            # Email to Customer
            cust_html = render_to_string('emails/customer_reply.html', context)
            cust_msg = EmailMultiAlternatives(
                "Message Received - Columbia Limozn", 
                strip_tags(cust_html), 
                settings.DEFAULT_FROM_EMAIL, 
                [email]
            )
            cust_msg.attach_alternative(cust_html, "text/html")
            cust_msg.send(fail_silently=False)

            messages.success(request, "Your message has been sent. Thank you for contacting us!")
            return redirect('index')

    return render(request, 'taxi/index.html')
    



from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Reservation # Ensure this is imported

def make_reservation(request):
    if request.method == "POST":
        # Combine Time Fields
        hh = request.POST.get('hh')
        mm = request.POST.get('mm')
        ampm = request.POST.get('ampm')
        full_time = f"{hh}:{mm} {ampm}"

        res = Reservation.objects.create(
            name=request.POST.get('name'),
            date_of_service=request.POST.get('date'),
            pickup_time=full_time,
            pickup_address=request.POST.get('from'),
            dropoff_location=request.POST.get('to'),
            email=request.POST.get('email'),
            mobile_contact=request.POST.get('mobile'),
            company_name=request.POST.get('company'),
            special_notes=request.POST.get('notes'),
        )

        # Email Logic - Pull from settings.py
        subject = 'Reservation Confirmation - Columbia Limousine Service'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Recipient list: The customer AND the admin
        recipient_list = [res.email, settings.ADMIN_EMAIL]

        html_content = render_to_string('emails/reservation_email.html', {'res': res})
        
        try:
            email = EmailMultiAlternatives(
                subject, 
                "New Reservation Details", 
                from_email, 
                recipient_list
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False) # fail_silently=False helps debug
            messages.success(request, "Your reservation has been submitted successfully!")
        except Exception as e:
            # This will show you the exact error in your console/logs
            print(f"Email Error: {e}")
            messages.error(request, "Reservation saved, but email confirmation failed.")

        return redirect('reservation_success')

    return render(request, 'taxi/reservation.html')

def reservation_success(request):
    return render(request, 'taxi/success.html')
    
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
    return render(request, 'taxi/contact.html')
    
def fleet(request):
    return render(request, 'taxi/fleet.html')
    
def service(request):
    return render(request, 'taxi/service.html')