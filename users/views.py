from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if 'vehicle_id' in request.session:
                    del request.session['vehicle_id']
                if 'garage_id' in request.session:
                    del request.session['garage_id']
                if 'booking_id' in request.session:
                    del request.session['booking_id']
                return redirect('home')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})

def sign_out(request):
    logout(request)
    if 'vehicle_id' in request.session:
        del request.session['vehicle_id']
    if 'garage_id' in request.session:
        del request.session['garage_id']
    if 'booking_id' in request.session:
        del request.session['booking_id']
    return redirect('home')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/register.html', {'form': form})