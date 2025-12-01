# userauths/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from userauths.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Please use a different email.")
            else:
                form.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("home")  # Change to login page URL if needed
        else:
            # Collect and display all form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=email, password=password)  # use email as username if your User model uses email as USERNAME_FIELD

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")  # Redirect after login
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")   # redirect to login page (change if needed)