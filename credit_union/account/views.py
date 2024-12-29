from django.shortcuts import render, HttpResponse
from .models import *
from django.db.models import F, Sum, Count, Avg, Max, Min

# Create your views here.
def home(request):
    return render(request, "home.html", {"current_year": 2024})

def add_member(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        msisdn = request.POST.get("phone")
        email = request.POST.get("email")
        dob = request.POST.get("dob")
        id_type = request.POST.get("id_type")
        all_members = [member.msisdn for member in Member.objects.all()]
        if int(msisdn) in all_members:
            return HttpResponse("Member already exists")
        else:
            member = Member.objects.create(msisdn=msisdn)
            details = KYCDetails.objects.create(member_msisdn=member, first_name=first_name, last_name=last_name, email=email, dob=dob, id_type=id_type)
        
        return HttpResponse("Member added successfully")
    return render(request, "add_member.html", {"current_year": 2024})

def input_loans(request):
    return render(request, "input_loans.html", {"current_year": 2024})

def make_contribution(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), last_name=F("kycdetails__last_name"))
    if request.method == "POST":
        name = request.POST.get("member")
        amount = float(request.POST.get("amount"))
        date = request.POST.get("date")
        one = name.split(" ")
        try:
            member = Member.objects.get(kycdetails__first_name=one[0], kycdetails__last_name=one[1])
        except Member.DoesNotExist:
            return HttpResponse("Member not found")
        Contribution.objects.create(member_msisdn=member, amount=amount, transaction_date=date)
        return HttpResponse("Contribution made successfully")

    return render(request, "make_contribution.html", {"current_year": 2024, "members": members})

def view_members(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), last_name=F("kycdetails__last_name"), total_contribution=Sum("contribution__amount"), loan_debt=Sum("approvedloan__amount_left"))
    return render(request, "view_members.html", {"current_year": 2024, "members": members})

def view_history(request):
    return render(request, "history.html", {"current_year": 2024})
