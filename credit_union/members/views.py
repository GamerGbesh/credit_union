from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from account.models import CreditUnionBalance
from account.forms import CustomUserCreationForm



# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    return render(request, "authentication/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("login")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username").lower()
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username.lower(), password=password)
            messages.success(request, "Account created successfully")
            login(request, user)
            user = request.user
            CreditUnionBalance.objects.create(user_id=user)
            return redirect("home")
            
    else:
        form = CustomUserCreationForm()
    return render(request, "authentication/signup.html", {"form": form})


