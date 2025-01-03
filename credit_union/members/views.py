from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from account.models import CreditUnionBalance
from django.contrib.auth.models import User


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
        # username = request.POST.get("username").lower()
        # email = request.POST.get("email")
        # password = request.POST.get("password")
        # validate_password = request.POST.get("password2")

        # if len(password) < 8:
        #     messages.error(request, "Password is less than 8 characters")
        #     return render(request, "authentication/signup.html", {"red":True})
        # if username in password.lower():
        #     messages.error(request, "Password is too similar to username")
        #     return render(request, "authentication/signup.html", {"red":True})
        # if password != validate_password:
        #     messages.error(request, "Passwords do not match!")
        #     return render(request, "authentication/signup.html", {"red":True})
        # if User.objects.filter(username=username).exists():
        #     messages.error(request, "Username already exists")
        #     return redirect("signup")
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Email already exists")
        #     return redirect("signup")
        # user = User.objects.create_user(username=username, email=email, password=password)
        # user.save()

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            messages.success(request, "Account created successfully")
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "authentication/signup.html", {"form": form})


def create_union(request):
    if request.method == "POST":
        union_name = request.POST.get("name")
        if len(union_name) > 50:
            messages.error(request, "Name is too long")
            return redirect("create_union")
        user = request.user
        CreditUnionBalance.objects.create(name=union_name, user_id=user)
        return redirect("home")
    return render(request, "authentication/credit_union.html")