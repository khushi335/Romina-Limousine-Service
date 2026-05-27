from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("",index,name="index"),
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('reservation/success/<str:confirmation_number>/', views.booking_confirmation, name='reservation_success'),
    path('reservations/paypal-process/', views.paypal_process, name='paypal_process'),
    path('reservations/paypal-return/', views.paypal_return, name='paypal_return'),
    path('reservations/paypal-cancel/', views.paypal_cancel, name='paypal_cancel'),
    path("stripe-success/", views.stripe_success, name="stripe_success"),
    path("reservation/<uuid:confirmation_number>/", views.booking_confirmation, name="booking_confirmation"),
    path('areas-we-serve/', cities_served, name='cities_served'),
    path('service/', views.service, name='service'),
    path('fleet/', views.fleet, name='fleet'),
    path('contact/', views.contact, name='contact'),
    path('our-rate/', views.our_rate, name='our_rate'),
]
