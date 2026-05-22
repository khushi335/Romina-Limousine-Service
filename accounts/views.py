"""
Views for authentication and profile management.
Handles login, logout, registration, password change, and profile updates.
"""

import re
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect

# from .forms import ProfileForm
from .models import CustomUser,UserProfile

logger = logging.getLogger('django')

def log_in(request):
    """
    Authenticate and log in the user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', '')

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is not registered yet')
            return redirect('log_in')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session.set_expiry(1209600 if remember_me else 0)

            try:
                send_mail(
                    subject='Login Notification',
                    message=f'Hi {user.first_name},\n\nYou have successfully logged in.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.warning(f"Login email failed: {e}")

            if user.is_head:
                return redirect('index')
            if user.is_user:
                return redirect('index')

            next_page = request.POST.get('next', '')
            return redirect(next_page or 'index')

        messages.error(request, 'Invalid password!')
        return redirect('log_in')

    next_page = request.GET.get('next', '')
    return render(request, 'auth/login.html', {'next': next_page})


def register(request):
    """
    Register a new user with validation.
    """
    if request.method == 'POST':
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')
        role = request.POST.get('role')
        is_head = role == 'head'

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            validate_password(password)

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username is already registered!")
                return redirect('register')

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered!")
                return redirect('register')

            if username == password:
                messages.error(request, "Username and password shouldn't be the same.")
                return redirect('register')

            if not re.search(r'[A-Z]', password):
                messages.error(request, "Password must contain at least one uppercase letter.")
                return redirect('register')

            if not re.search(r'\W', password):
                messages.error(request, "Password must contain at least one special character.")
                return redirect('register')

            if not re.search(r'\w', password):
                messages.error(request, "Password must contain alphanumeric characters.")
                return redirect('register')

            user = CustomUser.objects.create_user(
                first_name=fname,
                last_name=lname,
                username=username,
                phone=phone,
                address=address,
                email=email,
                password=password,
                is_landlord=is_head,
            )
            UserProfile.objects.create(user=user, role=role)

            send_mail(
                subject='Welcome to Our Platform!',
                message=f'Hi {fname},\n\nThank you for registering with us.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! Please check your email.")
            return redirect('log_in')

        except Exception as e:
            logger.error(f"Registration error: {e}")
            messages.error(request, str(e))
            return redirect('register')

    return render(request, "auth/register.html")


def log_out(request):
    """
    Log out the current user.
    """
    logout(request)
    return redirect('log_in')


@login_required(login_url='log_in')
def change_password(request):
    """
    Allow user to change password.
    """
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('log_in')

    return render(request, 'auth/change_password.html', {'form': form})


# @login_required(login_url='log_in')
# def profile(request):
#     """
#     Display user profile.
#     """
#     return render(request, 'profile/profile.html')


# @login_required(login_url='log_in')
# def update_profile(request):
#     """
#     Update user's profile and notify them via email.
#     """
#     profile, _ = ProfileData.objects.get_or_create(user=request.user)
#     form = ProfileForm(instance=profile)

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()

#             try:
#                 send_mail(
#                     subject='Profile Updated Successfully',
#                     message=f'Hi {request.user.first_name},\n\nYour profile has been updated.',
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[request.user.email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 logger.warning(f"Profile update email failed: {e}")

#             messages.success(request, "Profile updated successfully.")
#             return redirect('profile')

#     user_reviews = Review.objects.filter(user=request.user).select_related('property')

#     context = {
#         'form': form,
#         'user': request.user,
#         'profile': request.user.profile,
#         'user_reviews': user_reviews,
#     }
#     return render(request, 'profile/update_profile.html', context)
