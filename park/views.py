from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Booking, Vehicles, Garages
from .booking_for_display import BookingForDisplay
from .forms import BookingForm, VehicleForm


def home(request):
    if 'vehicle_id' in request.session:
        del request.session['vehicle_id']
    if 'garage_id' in request.session:
        del request.session['garage_id']
    if 'booking_id' in request.session:
        del request.session['booking_id']
    context = {}
    if request.user.is_authenticated:
        garages = Garages.objects.all()
        vehicles = Vehicles.objects.filter(user=request.user)
        context['vehicles'] = vehicles
        bookings = Booking.objects.filter(user=request.user)
        if bookings:
            booking_list = list()
            for booking in bookings:
                vehicle = list(filter(lambda v: v.id == booking.vehicle_id, vehicles))[0]
                garage = list(filter(lambda g: g.id == booking.parking_garage_id, garages))[0]
                b = BookingForDisplay(garage.name, vehicle.tag_number, booking.start_time, booking.end_time, booking.status, booking.id)
                booking_list.append(b)
            context['bookings'] = booking_list

    return render(request, 'park/home.html', context)

@login_required
def create(request):
    context = {}
    queryset = Vehicles.objects.filter(user=request.user)
    v = get_object_or_404(queryset, pk=request.session['vehicle_id'])
    context['vehicle'] = v
    queryset = Garages.objects.filter(id=request.session['garage_id'])
    g = get_object_or_404(queryset)
    context['garage'] = g
    if request.method == 'GET':
        context['form'] = BookingForm()
        return render(request, 'park/create_booking_form.html', context)
    elif request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.parking_garage_id=request.session['garage_id']
            booking.vehicle_id=request.session['vehicle_id']
            booking.status="BOOKED"
            booking.save()
            g.remaining_capacity -= 1
            g.save()
            del request.session['vehicle_id']
            del request.session['garage_id']
            messages.success(request, 'Booked successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the following errors:')
            context['form'] = form
            return render(request, 'park/create_booking_form.html', context)

@login_required
def cancel(request, id):
    queryset = Booking.objects.filter(user=request.user)
    booking = get_object_or_404(queryset, pk=id)
    context = {'booking': booking}

    if request.method == 'GET':
        return render(request, 'park/booking_confirm_delete.html', context)
    elif request.method == 'POST':
        booking.delete()
        messages.success(request, 'The booking has been canceled successfully.')
        return redirect('home')

@login_required
def detail(request, id):
    queryset = Booking.objects.filter(user=request.user)
    booking = get_object_or_404(queryset, id=id)
    context = {'booking': booking}
    queryset = Vehicles.objects.filter(user=request.user)
    v = get_object_or_404(queryset, pk=booking.vehicle_id)
    context['vehicle'] = v
    queryset = Garages.objects.filter(id=booking.parking_garage_id)
    g = get_object_or_404(queryset)
    context['garage'] = g
    request.session['vehicle_id'] = v.id
    request.session['garage_id'] = g.id
    request.session['booking_id'] = booking.id
    return render(request, 'park/detail.html', context)

@login_required
def park(request, id):
    queryset = Booking.objects.filter(user=request.user)
    booking = get_object_or_404(queryset, id=id)
    if booking.status == "BOOKED":
        booking.status = "PARKED"
        booking.save()
        messages.success(request, 'Parked!')
    else:
        messages.error(request, 'Booking is not in correct state')
    return redirect('home')

@login_required
def exit(request, id):
    queryset = Booking.objects.filter(user=request.user)
    booking = get_object_or_404(queryset, id=id)
    if booking.status == "PARKED":
        booking.status = "EXITED"
        booking.save()
        queryset = Garages.objects.filter(id=booking.parking_garage_id)
        g = get_object_or_404(queryset)
        g.remaining_capacity += 1
        g.save()
        messages.success(request, 'Done!')
    else:
        messages.error(request, 'Booking is not in correct state')
    return redirect('home')

@login_required
def edit(request, id):
    queryset = Booking.objects.filter(user=request.user)
    booking = get_object_or_404(queryset, id=id)
    context = {}
    queryset = Vehicles.objects.filter(user=request.user)
    v = get_object_or_404(queryset, pk=request.session['vehicle_id'])
    context['vehicle'] = v
    queryset = Garages.objects.filter(id=request.session['garage_id'])
    g = get_object_or_404(queryset)
    context['garage'] = g
    context['id'] = id
    if request.method == 'GET':
        context['form'] = BookingForm(instance=booking)
        return render(request,'park/create_booking_form.html',context)
    elif request.method == 'POST':
        print(f'original = {booking.id}')
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            print(f'booking garage: {booking.parking_garage_id}')
            print(f'ne garage: {g.id}')
            if booking.parking_garage_id != g.id:
                g.remaining_capacity -= 1
                g.save()
                queryset = Garages.objects.filter(id=booking.parking_garage_id)
                old_garage = get_object_or_404(queryset)
                old_garage.remaining_capacity += 1
                old_garage.save()
                booking.parking_garage_id = g.id
            if booking.vehicle_id != v.id:
                booking.vehicle_id = v.id
            booking.save()
            messages.success(request, 'The booking has been updated successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the following errors:')
            context['form'] = form
            return render(request, 'park/create_booking_form.html', context)

@login_required
def add_vehicle(request):
    if request.method == 'GET':
        context = {'form': VehicleForm()}
        return render(request, 'park/add_vehicle_form.html', context)
    elif request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            messages.success(request, 'Vehicle added successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'park/add_vehicle_form.html', {'form': form})

@login_required
def remove_vehicle(request, id):
    queryset = Vehicles.objects.filter(user=request.user)
    vehicle = get_object_or_404(queryset, pk=id)
    context = {'vehicle': vehicle}

    if request.method == 'GET':
        return render(request, 'park/vehicle_confirm_delete.html', context)
    elif request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'The vehicle has been removed successfully.')
        return redirect('home')

@login_required
def select_vehicle(request):
    context = {}
    context['vehicles'] = Vehicles.objects.filter(user=request.user)
    if request.method == 'GET':
        if 'vehicle_id' in request.session:
            context['selected_id'] = request.session['vehicle_id']
        return render(request, 'park/select_vehicle.html', context)
    elif request.method == 'POST':
        vehicle_id = int(request.POST.get('selectedid'))
        request.session['vehicle_id'] = vehicle_id
        return redirect('select-garage')

@login_required
def select_garage(request):
    context = {'garages': Garages.objects.all()}
    vehicle_id = request.session['vehicle_id']
    if 'garage_id' in request.session:
        context['selected_id'] = request.session['garage_id']
    queryset = Vehicles.objects.filter(user=request.user)
    v = get_object_or_404(queryset, pk=vehicle_id)
    context['vehicle'] = v
    if request.method == 'GET':
        return render(request, 'park/select_garage.html', context)
    elif request.method == 'POST':
        garage_id = int(request.POST.get('selectedid'))
        if 'booking_id' not in request.session or 'booking_id' in request.session and request.session['garage_id'] != garage_id:
            queryset = Garages.objects.filter(id=garage_id)
            g = get_object_or_404(queryset)
            if g.remaining_capacity == 0:
                messages.error(request, 'Garage not available')
                return render(request, 'park/select_garage.html', context)
        request.session['garage_id'] = garage_id
        if 'booking_id' in request.session:
            return redirect('edit-booking', request.session['booking_id'])
        else:
            return redirect('create-booking')