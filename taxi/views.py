from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from .models import Booking, ContactMessage, Reservation

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
    if request.method == "POST":
        # Combine Time Fields
        hh = request.POST.get('hh')
        mm = request.POST.get('mm')
        ampm = request.POST.get('ampm')
        full_time = f"{hh}:{mm} {ampm}"

        # Create the object
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

        # Email Logic
        subject = 'Reservation Confirmation - Romina Limousine Service'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Ensure recipient_list is a flat list
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'sahkhushi946@gmail.com')
        recipient_list = [res.email, admin_email]

        # Use 'reservation' as the key to match the template
        html_content = render_to_string('taxi/reservation_receipt.html', {'reservation': res})
        
        try:
            email = EmailMultiAlternatives(
                subject, 
                "New Reservation Details", 
                from_email, 
                recipient_list
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            messages.success(request, "Your reservation has been submitted successfully!")
        except Exception as e:
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