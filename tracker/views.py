from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, HabitForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import User, Habit



# Route: '/'
# Methods: GET 
# Desc: Home page that shows habits if user is logged in
def home(request):
    # Chech if user is authenticated
    if request.user.is_authenticated:
        habits = Habit.objects.filter(user_id=request.user.id)
        return render(request, 'tracker/home.html', {'habits': habits})

    return redirect('tracker:login_request')

# Route: '/register'
# Methods: GET, POST 
# Desc: Allow user to register
def register(request):
    # Chech if user is authenticated
    if request.user.is_authenticated:
        return redirect('tracker:home')
    
    # Method == POST
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # Validate form
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account created.')
            # Login user after registered
            login(request, user)
            messages.success(request, 'User logged in.')
            return redirect('tracker:home')
        else:
            # Handle form errors
            for msg in form.errors:
                messages.error(request, f"{msg}: {form.errors[msg]}")
        
    # Method == GET
    form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

# Route: '/login'
# Methods: GET, POST 
# Desc: Allow user to login
def login_request(request):
    # Chech if user is authenticated
    if request.user.is_authenticated:
        return redirect('tracker:home')

    # Method == POST
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # Validate form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, 'You are logged in.')
                return redirect('tracker:home')
            else:
                # Handle authetication errors
                messages.error(request, 'Invalid credentials.')
        else: 
            # Handle form errors
            messages.error(request, 'Invalid credentials.')
    
    # Method == GET
    form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

# Route: '/logout'
# Methods: GET
# Desc: Allow user to logout
def logout_request(request):
    logout(request)
    messages.info(request, 'You successfully logged out.')
    return redirect('tracker:home')

# Route: '/add-habit'
# Methods: GET, POST 
# Desc: Allow user to create a new habit
def add_habit(request):
    # Chech if user is authenticated
    if request.user.is_authenticated:
        return redirect('tracker:home')

    # Method == POST
    if request.method == 'POST':
        form = HabitForm(request.POST)
        # Validate form
        if form.is_valid():
            # Get form data
            activity = form.cleaned_data.get('activity')
            time_spent = form.cleaned_data.get('time_spent')
            description = form.cleaned_data.get('description')
            # Get user
            user = User.objects.get(id=request.user.id)
            # Create new instance of Habit
            new_habit = Habit(activity=activity, time_spent=time_spent, description=description, user_id=user)
            # Save the new instance
            new_habit.save()
            messages.success(request, 'Activity added successfully.')
            return redirect('tracker:home')
        else:
            # Handle form errors
            messages.error(request, 'Something went wrong. Please try again.')

    # Method == GET       
    form = HabitForm()
    return render(request, 'tracker/add-habit.html', {'form': form, 'title': 'Add activity'})

# Route: '/update-habit/habit_id'
# Methods: GET, POST 
# Desc: Allow user to update a specific habit
def update_habit(request, habit_id):
    # Chech if user is authenticated
    if request.user.is_authenticated:
        return redirect('tracker:home')
    
    # Get the passed habit and the user
    habit = Habit.objects.get(id=habit_id)
    user = User.objects.get(id=request.user.id)

    # Check if habit exists
    if habit is None:
        messages.error(request, 'This habit does not exist.')
        return redirect('tracker:home')
    # Check if the user owns this habit
    if habit.user_id != user:
        messages.error(request, 'You are not allowed to perform this action.')
        return redirect('tracker:home')

    # Method == POST
    if request.method == 'POST':
        form = HabitForm(request.POST)
        # Validate form
        if form.is_valid():
            # Update current habit
            habit.activity = form.cleaned_data.get('activity')
            habit.time_spent = form.cleaned_data.get('time_spent')
            habit.description = form.cleaned_data.get('description')
            # Save the updated habit
            habit.save()
            messages.success(request, 'Activity updated successfully.')
            return redirect('tracker:home')
        else:
             # Handle form errors
            messages.error(request, 'Something went wrong. Please try again.')

    # Method == GET
    form = HabitForm()
    # Populate the input fields with the current values
    form.fields['activity'].initial = habit.activity
    form.fields['time_spent'].initial = habit.time_spent
    form.fields['description'].initial = habit.description
    return render(request, 'tracker/add-habit.html', {'form': form, 'title': 'Update activity'})

# Route: '/delete-habit/habit_id'
# Methods: GET, POST 
# Desc: Allow user to delete a specific habit
def delete_habit(request, habit_id):
    # Chech if user is authenticated
    if request.user.is_authenticated:
        return redirect('tracker:home')

    # Get the passed habit and the user
    habit = Habit.objects.get(id=habit_id)
    user = User.objects.get(id=request.user.id)

    # Check if habit exists
    if habit is None:
        messages.error(request, 'This habit does not exist.')
        return redirect('tracker:home')
    # Check if the user owns this habit
    if habit.user_id != user:
        messages.error(request, 'You are not allowed to perform this action.')
        return redirect('tracker:home')

    # Delete the habit from the database
    habit.delete()
    messages.success(request, 'Activity successfully deleted.')
    return redirect('tracker:home')