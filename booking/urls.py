from django.urls import path 
from . import views 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_control
urlpatterns=[ 
    path('', views.home, name='home'),
    path('hotel_list/', views.hotel_list, name='hotel_list'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('restaurant_list/', views.restaurant_list, name='restaurant_list'),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
    path('book_hotel/', views.book_hotel, name='book_hotel'),
    path('booking_hotel_success/', views.booking_hotel_success, name='booking_hotel_success'),
    path('book_movie/', views.book_movie, name='book_movie'),
    path('booking_success/',views.booking_success,name='booking_success'),
    path('book_restaurant/', views.book_restaurant, name='book_restaurant'),
    path('booking_dinning_success/', views.booking_dinning_success, name='booking_dinning_success'),
]