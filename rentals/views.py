from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from .forms import CustomUserCreationForm, AvailabilityForm, BookingConfirmationForm
from .models import Car, Booking


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    bookings = Booking.objects.all().order_by('-start_date')
    context = {
        'bookings': bookings
    }
    return render(request, 'rentals/admin_dashboard.html', context)


@user_passes_test(lambda u: u.is_staff)
def cancel_booking_view(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.is_approved = False
        booking.save()
        messages.success(request, f"Booking for {booking.car.name} by {booking.user.username} has been canceled.")
    return redirect('admin_dashboard')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'rentals/login.html', {'form': form})


def home_view(request):
    form = AvailabilityForm()
    return render(request, 'rentals/home.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='rentals.backends.EmailOrUsernameBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rentals/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def car_list_view(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    capacity = request.GET.get('capacity')

    # If someone opens /cars/ directly without searching, send them to the search form
    if not (start_date_str and end_date_str and capacity):
        return redirect('home')

    # Only approved (not canceled) bookings block a car
    booked_car_ids = Booking.objects.filter(
        Q(start_date__lte=end_date_str) & Q(end_date__gte=start_date_str),
        is_approved=True,
    ).values_list('car_id', flat=True)

    available_cars = Car.objects.filter(
        capacity__gte=capacity
    ).exclude(
        id__in=booked_car_ids
    )

    context = {
        'cars': available_cars,
        'start_date': start_date_str,
        'end_date': end_date_str
    }
    return render(request, 'rentals/car_list.html', context)


@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    context = {
        'bookings': bookings,
        'today': timezone.now().date(),  # used by the template for the cancellation rule
    }
    return render(request, 'rentals/dashboard.html', context)


@login_required
def confirm_booking_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    duration = (end_date - start_date).days + 1
    total_cost = duration * car.price_per_day

    initial_data = {
        'full_name': request.user.profile.full_name,
        'date_of_birth': request.user.profile.date_of_birth,
        'license_number': request.user.profile.license_number,
    }

    if request.method == 'POST':
        form = BookingConfirmationForm(request.POST, initial=initial_data)
        if form.is_valid():
            profile = request.user.profile
            profile.full_name = form.cleaned_data['full_name']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.license_number = form.cleaned_data['license_number']
            profile.save()

            # Create the booking
            booking = Booking.objects.create(
                user=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
                total_cost=total_cost
            )
            return render(request, 'rentals/booking_confirmation.html', {'booking': booking})
    else:
        form = BookingConfirmationForm(initial=initial_data)

    context = {
        'car': car,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'total_cost': total_cost,
        'form': form
    }
    return render(request, 'rentals/confirm_booking.html', context)


@login_required
def my_cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Security check
    cancellation_deadline = booking.start_date - timedelta(days=2)

    if request.method == 'POST':
        if timezone.now().date() <= cancellation_deadline:
            booking.is_approved = False
            booking.save()
            messages.success(request, "Your booking has been successfully canceled.")
        else:
            messages.error(request, "Cancellation is not allowed within 48 hours of the start date.")
        return redirect('dashboard')

    return redirect('dashboard')
