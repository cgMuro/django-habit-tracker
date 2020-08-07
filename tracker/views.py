from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, HabitForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import User, Habit




def home(request):
    if request.user.is_authenticated:
        habits = Habit.objects.filter(user_id=request.user.id)
        return render(request, 'tracker/home.html', {'habits': habits})

    return redirect('tracker:login_request')

def register(request):
    if request.user.is_authenticated:
        return redirect('tracker:home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account created.')
            login(request, user)
            messages.success(request, 'User logged in.')
            return redirect('tracker:home')
        else:
            for msg in form.errors:
                messages.error(request, f"{msg}: {form.errors[msg]}")
    return render(request, 'tracker/register.html', {'form': form})

def login_request(request):
    if request.user.is_authenticated:
        return redirect('tracker:home')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, 'You are logged in.')
                return redirect('tracker:home')
            else:
                messages.error(request, 'Invalid credentials.')
        else: 
            messages.error(request, 'Invalid credentials.')

    return render(request, 'tracker/login.html', {'form': form})

def logout_request(request):
    logout(request)
    messages.info(request, 'You successfully logged out.')
    return redirect('tracker:home')

def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            activity = form.cleaned_data.get('activity')
            time_spent = form.cleaned_data.get('time_spent')
            description = form.cleaned_data.get('description')
            user = User.objects.get(id=request.user.id)
            new_habit = Habit(activity=activity, time_spent=time_spent, description=description, user_id=user)
            new_habit.save()
            messages.success(request, 'Activity added successfully.')
            return redirect('tracker:home')
        else:
            messages.error(request, 'Something went wrong. Please try again.')
            
    form = HabitForm()
    return render(request, 'tracker/add-habit.html', {'form': form, 'title': 'Add activity'})

def update_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    user = User.objects.get(id=request.user.id)

    if habit.user_id != user:
        messages.error(request, 'You are not allowed to perform this action.')
        return redirect('tracker:home')

    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit.activity = form.cleaned_data.get('activity')
            habit.time_spent = form.cleaned_data.get('time_spent')
            habit.description = form.cleaned_data.get('description')
            habit.save()
            messages.success(request, 'Activity updated successfully.')
            return redirect('tracker:home')
        else:
            messages.error(request, 'Something went wrong. Please try again.')

    form = HabitForm()
    form.fields['activity'].initial = habit.activity
    form.fields['time_spent'].initial = habit.time_spent
    form.fields['description'].initial = habit.description
    return render(request, 'tracker/add-habit.html', {'form': form, 'title': 'Update activity'})

def delete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    user = User.objects.get(id=request.user.id)
    if habit is None:
        messages.error(request, 'This habit does not exist.')
        return redirect('tracker:home')
    if habit.user_id != user:
        messages.error(request, 'You are not allowed to perform this action.')
        return redirect('tracker:home')

    habit.delete()
    messages.success(request, 'Activity successfully deleted.')
    return redirect('tracker:home')