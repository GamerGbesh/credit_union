from django.shortcuts import render, HttpResponse


class member():
    def __init__(self, msisdn, name):
        self.msisdn = msisdn
        self.name = name

# Create your views here.
def home(request):
    return render(request, "home.html", {"current_year": 2024})

def add_member(request):
    return render(request, "add_member.html", {"current_year": 2024})

def input_loans(request):
    return render(request, "input_loans.html", {"current_year": 2024})

def make_contribution(request):
    return render(request, "make_contribution.html", {"current_year": 2024, "members": [member("1234567890", "John Doe"), member("1234567891", "Jane Doe")]})

def view_members(request):
    return render(request, "view_members.html", {"current_year": 2024})

def view_history(request):
    return render(request, "history.html", {"current_year": 2024})
