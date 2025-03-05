from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied

from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from .models import Record


def home(request):
    """Render homepage with login/register options."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'webapp/index.html')


def register(request):
    """Handle user registration with enhanced error messaging."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    messages.success(
                        request, f"Welcome, {user.username}! Your account has been created.")
                    return redirect("my-login")
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")

    return render(request, 'webapp/register.html', {'form': form})


def my_login(request):
    """Enhanced login view with clear error messaging."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'webapp/my-login.html', {'form': form})


@login_required(login_url='my-login')
def dashboard(request):
    """Enhanced dashboard with sorting and filtering."""
    records = Record.objects.all().order_by('-creation_date')
    context = {'records': records}
    return render(request, 'webapp/dashboard.html', context)


@login_required(login_url='my-login')
def create_record(request):
    """Create record with enhanced validation and error handling."""
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            try:
                record = form.save()
                messages.success(
                    request, f"Record for {record.first_name} {record.last_name} created successfully!")
                return redirect("dashboard")
            except Exception as e:
                messages.error(request, f"Error creating record: {str(e)}")

    return render(request, 'webapp/create-record.html', {'form': form})


@login_required(login_url='my-login')
def update_record(request, pk):
    """Update record with enhanced error handling."""
    record = get_object_or_404(Record, id=pk)

    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            try:
                updated_record = form.save()
                messages.success(
                    request, f"Record for {updated_record.first_name} {updated_record.last_name} updated successfully!")
                return redirect("dashboard")
            except Exception as e:
                messages.error(request, f"Error updating record: {str(e)}")

    return render(request, 'webapp/update-record.html', {'form': form})


@login_required(login_url='my-login')
def singular_record(request, pk):
    """View single record with 404 handling."""
    record = get_object_or_404(Record, id=pk)
    return render(request, 'webapp/view-record.html', {'record': record})


@login_required(login_url='my-login')
def delete_record(request, pk):
    """Delete record with enhanced error handling."""
    record = get_object_or_404(Record, id=pk)

    try:
        record_name = f"{record.first_name} {record.last_name}"
        record.delete()
        messages.success(
            request, f"Record for {record_name} deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting record: {str(e)}")

    return redirect("dashboard")


def user_logout(request):
    """Logout with success message."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("my-login")
