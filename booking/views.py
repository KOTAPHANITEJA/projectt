from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import CreateUserForm #,BookingForm
#from .models import Hotel, Booking
import csv
from django.contrib import messages
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request): 
    return render(request,'home.html',{'name':'Passengers'})

def hotel_list(request):
    df = pd.read_csv("booking\hotels.csv")
    return render(request, 'hotel_list.html', {'hotels_table': df.to_html()})

def movie_list(request):
    df= pd.read_csv("booking\mov.csv")
    return render(request, 'movie_list.html',{'movies_table':df.to_html()})

def restaurant_list(request):
    df=pd.read_csv("booking\dining.csv")
    return render(request, 'restaurant_list.html',{'restaurants_table':df.to_html()})

def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutPage(request):
    logout(request)
    return redirect('login')


def book_hotel(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        num_rooms = request.POST.get('num_rooms')

        # Read hotels data from CSV file
        hotels_data = pd.read_csv('booking/hotels.csv')

        # Strip whitespace and ensure hotel_id is a string
        hotels_data['hotel_id'] = hotels_data['hotel_id'].astype(str).str.strip()

        # Find the hotel with the matching ID
        hotel_data = hotels_data[hotels_data['hotel_id'] == hotel_id]
        print(f"Hotels_Data: {hotels_data}")

        if hotel_data.empty:
            messages.error(request, 'Hotel not found!')
            return redirect('book_hotel')
        else:
            # Pass hotel details to the booking success page
            data={
                'hotel_name': hotel_data.iloc[0]["hotel_name"], # Assuming 'hotel_name' is the column name
                'hotel_area': hotel_data.iloc[0]["hotel_area"],
                'category': hotel_data.iloc[0]["category"],
                'checkin_date': checkin_date,
                'checkout_date': checkout_date,
                'num_rooms': num_rooms
            }
            return render(request, 'booking_hotel_success.html', data)
    else:
        # For GET request, display the list of hotels
        hotels_data = pd.read_csv('booking/hotels.csv')
        return render(request, 'book_hotel.html', {'hotels': hotels_data.to_dict('records')})

def booking_hotel_success(request):
    return render(request, 'booking_hotel_success.html')

def book_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        show_time = request.POST.get('show_time')
        num_tickets = request.POST.get('num_tickets')
        
        print(f"Movie ID: {movie_id}")
        print(f"Show Time: {show_time}")
        print(f"Number of Tickets: {num_tickets}")
        
        # Read movies data from CSV file
        movies_data = pd.read_csv('booking/mov.csv')

        # Print the columns for debugging
        print("Columns:", movies_data.columns)

        # Strip whitespace and ensure movie_id is a string
        movies_data['movie_id'] = movies_data['movie_id'].astype(str).str.strip()

        # Print available movie IDs for debugging
        print("Available Movie IDs after processing:", movies_data['movie_id'].unique())

        # Find the movie with the matching ID
        movie_data = movies_data[movies_data['movie_id'] == movie_id]

        print(f"Movie Data: {movie_data}")

        if movie_data.empty:
            print("Movie not found!")
            messages.error(request, 'Movie not found!')
            return redirect('book_movie')
        else:
             messages.success(request, f'Booking successful for {movie_data.iloc[0]["movie_name"]} at {movie_data.iloc[0]["theatre_name"]}!')
             return render(request, 'booking_success.html', {
                'movie_name': movie_data.iloc[0]["movie_name"],
                'theatre_name': movie_data.iloc[0]["theatre_name"],
                'show_time': show_time,
                'num_tickets': num_tickets
            })
    else:
        # Read movies data from CSV file
        movies_data = pd.read_csv('booking/mov.csv')
        
        # Render the book movie page with the movies data
        return render(request, 'book_movie.html', {'movies': movies_data.to_dict('records')})
    

def booking_success(request):
    return render(request, 'booking_success.html')


def book_restaurant(request):
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        booking_date = request.POST.get('booking_date')
        num_guests = request.POST.get('num_guests')

        # Read restaurant data from CSV file
        restaurants_data = pd.read_csv('booking/dining.csv')

        # Strip whitespace and ensure restaurant_id is a string
        restaurants_data['restaurant_id'] = restaurants_data['restaurant_id'].astype(str).str.strip()

        # Find the restaurant with the matching ID
        restaurant_data = restaurants_data[restaurants_data['restaurant_id'] == restaurant_id]
        print(f"Restaurant_data: {restaurant_data}")

        if restaurant_data.empty:
            messages.error(request, 'Restaurant not found!')
            return redirect('book_restaurant')
        else:
            # Pass restaurant details to the booking success page
            data= {
                'restaurant_name': restaurant_data.iloc[0]["restaurant_name"], # Assuming 'restaurant_name' is the column name
                'Area':  restaurant_data.iloc[0]["Area"],
                'Address': restaurant_data.iloc[0]["Address"],
                'Cuisine':  restaurant_data.iloc[0]["Cuisine"],
                'booking_date': booking_date,
                'num_guests': num_guests
            }
            return render(request, 'booking_dinning_success.html',data)
    else:
        # For GET request, display the list of restaurants
        restaurants_data = pd.read_csv('booking/dining.csv')
        return render(request, 'book_restaurant.html', {'restaurants': restaurants_data.to_dict('records')})
    

def booking_dinning_success(request):
    return render(request, 'booking_dinning_success.html')
