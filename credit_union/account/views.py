from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import *
from django.db.models import F, Sum, Count, Avg, Max, Min
from datetime import datetime

# Create your views here.

# Members
def home(request):

    return render(request, "home.html", {"current_year": 2024})

def add_member(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        msisdn = request.POST.get("phone")
        email = request.POST.get("email")
        if not email:
            email = None
        dob = request.POST.get("dob")
        id_type = request.POST.get("id_type")
        amount = request.POST.get("amount")
        if not amount:
            amount = 0
        all_members = [member.msisdn for member in Member.objects.all()]
        if int(msisdn) in all_members:
            return HttpResponse("Member already exists")
        else:
            member = Member.objects.create(msisdn=msisdn)
            KYCDetails.objects.create(member_msisdn=member, first_name=first_name, last_name=last_name, email=email, dob=dob, id_type=id_type)
            
        return redirect("view_members")
    return render(request, "add_member.html", {"current_year": 2024})

def view_members(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), 
                                      last_name=F("kycdetails__last_name"), 
                                      total_contribution=Sum("contribution__amount"), 
                                      loan_debt=Sum("approvedloan__amount_left"))
    credit_union_balance = CreditUnionBalance.objects.first()
    total_contributions = Contribution.objects.aggregate(Sum("amount"))["amount__sum"]
    total_loans = ApprovedLoan.objects.aggregate(Sum("amount_left"))["amount_left__sum"]
    if not credit_union_balance:
        credit_union_balance = 0
        CreditUnionBalance.objects.create(amount=credit_union_balance)
    else:
        credit_union_balance = credit_union_balance.amount
    if not total_contributions:
        total_contributions = 0
    if not total_loans:
        total_loans = 0
    return render(request, "view_members.html", {"current_year": 2024, "members": members, 
                                                 "credit_union_balance": credit_union_balance, 
                                                 "total_contribution": total_contributions, 
                                                 "total_loan_debt": total_loans})



def member_info(request, msisdn):
    member = Member.objects.annotate(first_name=F("kycdetails__first_name"), 
                                     last_name=F("kycdetails__last_name"), 
                                     total_contribution=Sum("contribution__amount"), 
                                     loan_debt=Sum("approvedloan__amount_left"), 
                                     email=F("kycdetails__email"), 
                                     dob=F("kycdetails__dob"), 
                                     id_type=F("kycdetails__id_type")).get(msisdn=msisdn)
    return render(request, "member.html", {"current_year": 2024, "member": member})



def edit_member(request, msisdn):
    member = Member.objects.annotate(first_name=F("kycdetails__first_name"), 
                                     last_name=F("kycdetails__last_name"), 
                                     total_contribution=Sum("contribution__amount"), 
                                     loan_debt=Sum("approvedloan__amount_left"), 
                                     email=F("kycdetails__email"), 
                                     dob=F("kycdetails__dob"), 
                                     id_type=F("kycdetails__id_type")).get(msisdn=msisdn)
    
    if request.method == "POST":
        new_msisdn = int(request.POST.get("phone"))
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        id_type = request.POST.get("id_type")
        member_obj = Member.objects.get(msisdn=msisdn)
        member_obj.msisdn = new_msisdn
        member_obj.save()        
        kyc = get_object_or_404(KYCDetails, member_msisdn=member)
        kyc.email = email
        kyc.first_name = first_name
        kyc.last_name = last_name
        kyc.id_type = id_type
        kyc.member_msisdn = member_obj 
        kyc.save()        
        return redirect("members", msisdn=new_msisdn)
    return render(request, "edit_member.html", {"current_year": 2024, "member": member})



# Contributions
def make_contribution(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), last_name=F("kycdetails__last_name"))
    if request.method == "POST":
        name = request.POST.get("member")
        amount = float(request.POST.get("amount"))
        one = name.split(" ")
        try:
            member = Member.objects.get(kycdetails__first_name=one[0], kycdetails__last_name=one[1])
        except Member.DoesNotExist:
            return HttpResponse("Member not found")
        Contribution.objects.create(member_msisdn=member, amount=amount)
        
        Transaction.objects.create(member_msisdn=member, transaction_type="DEPOSIT", amount=amount, description="Contribution")
        CreditUnionBalance.objects.update(amount=F("amount") + amount)
        return redirect("view_members")

    return render(request, "make_contribution.html", {"current_year": 2024, "members": members})





# History
def view_history(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), 
                                      last_name=F("kycdetails__last_name"), 
                                      transaction_type=F("transaction__transaction_type"), 
                                      date=F("transaction__created"), description=F("transaction__description"), 
                                      amount=F("transaction__amount"),
                                      transaction_created=F("transaction__created")).filter(amount__gt=0).order_by("-transaction_created")
    return render(request, "history.html", {"current_year": 2024, "members": members})



# Loans
def loan_request(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), 
                                      last_name=F("kycdetails__last_name"), 
                                      amount_requested=F("loanrequest__amount_requested"), 
                                      loan_status=F("loanrequest__status"), 
                                      date=F("loanrequest__request_date"), 
                                      loan_id=F("loanrequest__id"),
                                      loan_created=F("loanrequest__created")).filter(amount_requested__gt=0).order_by("-loan_created")
    return render(request, "loans.html", {"current_year": 2024, "members": members})





def loan_details(request, loan_id):
    loan = LoanRequest.objects.annotate(first_name=F("member_msisdn__kycdetails__first_name"), 
                                        last_name=F("member_msisdn__kycdetails__last_name"), 
                                        loan_description=F("loan_purpose"),
                                        loan_status=F("status"), 
                                        date=F("request_date"), 
                                        loan_id=F("id")).get(id=loan_id)
    member = Member.objects.get(msisdn=loan.member_msisdn.msisdn)
    try:
        approved = ApprovedLoan.objects.get(loan_request_id=loan)
    except ApprovedLoan.DoesNotExist:
        approved = None
    
    if request.method == "POST":
        value = request.POST.get("button")
        if value == "approve":
            loan.status = "APPROVED"
            loan.save()
            interest = 0.1 * float(loan.amount_requested)
            amount_to_deduct = float(loan.amount_requested) + interest
            year = datetime.now().year + 1
            month = datetime.now().month
            day = datetime.now().day
            due_date = datetime(year, month, day).date()
            member = Member.objects.get(msisdn=loan.member_msisdn.msisdn)
            ApprovedLoan.objects.create(member_msisdn=member,
                                        loan_request_id=loan, 
                                        amount_of_loan=loan.amount_requested, 
                                        interest=interest, 
                                        end_of_loan_date=due_date,
                                        monthly_deduction=amount_to_deduct/12,
                                        amount_left=amount_to_deduct)
            credit_union_balance = CreditUnionBalance.objects.first()
            credit_union_balance.amount = float(credit_union_balance.amount) - float(loan.amount_requested)
            credit_union_balance.save()
            Transaction.objects.create(member_msisdn=member, transaction_type="LOAN_WITHDRAWAL", amount=loan.amount_requested, description=loan.loan_description)
            approved = ApprovedLoan.objects.filter(loan_request_id=loan)
            
            
        elif value == "reject":
            loan.status = "REJECTED"
            loan.save()
        return redirect("loan_details", loan_id=loan_id)
        
    return render(request, "loan_details.html", {"current_year": 2024, "loan": loan, "approved": approved})

def input_loans(request):
    members = Member.objects.annotate(first_name=F("kycdetails__first_name"), last_name=F("kycdetails__last_name"))
    if request.method == "POST":
        name = request.POST.get("member")
        amount = float(request.POST.get("loan_amount"))
        one = name.split(" ")
        loan_purpose = request.POST.get("loan_purpose")
        try:
            member = Member.objects.get(kycdetails__first_name=one[0], kycdetails__last_name=one[1])
        except Member.DoesNotExist:
            return HttpResponse("Member not found")
        LoanRequest.objects.create(member_msisdn=member, amount_requested=amount, loan_purpose=loan_purpose)
        return redirect("loan_request")
    return render(request, "input_loans.html", {"current_year": 2024, "members": members})

def pay_loan(request, loan_id):
    loan = LoanRequest.objects.get(id=loan_id)
    approved = ApprovedLoan.objects.get(loan_request_id=loan)
    if request.method == "POST":
        amount_paid = float(request.POST.get("amount"))
        approved = ApprovedLoan.objects.get(loan_request_id=loan_id)
        approved.amount_left = float(approved.amount_left) - amount_paid
        approved.save()
        Transaction.objects.create(member_msisdn=loan.member_msisdn, transaction_type="LOAN_PAYMENT", amount=amount_paid, description="Loan payment")
        credit_union_balance = CreditUnionBalance.objects.first()
        credit_union_balance.amount = float(credit_union_balance.amount) + amount_paid
        credit_union_balance.save()
        return redirect("loan_details", loan_id=loan_id)
    return render(request, "pay_loan.html", {"current_year": 2024, "loan": loan})