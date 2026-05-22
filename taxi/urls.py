from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("",index,name="index"),
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    path('areas-we-serve/', cities_served, name='cities_served'),
    path('service/', views.service, name='service'),
    path('fleet/', views.fleet, name='fleet'),
    path('contact/', views.contact, name='contact'),
    # path('blog/', views.blog, name='blog'),
    # path('about', views.about, name='about'),
]
