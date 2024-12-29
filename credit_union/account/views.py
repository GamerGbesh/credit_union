from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def add_member(request):
    return render(request, "add_member.html")

def input_loans(request):
    return render(request, "input_loans.html")

def make_contribution(request):
    return render(request, "make_contribution.html")

def view_members(request):
    return render(request, "view_members.html")