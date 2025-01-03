from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import *
from django.db.models import F, Sum, DecimalField, DateTimeField, ExpressionWrapper
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required

# Create your views here.

# Members
def home(request):
    if request.user.is_authenticated:
        union = CreditUnionBalance.objects.filter(user_id=request.user).first()
        if union:
            total_contributions = Contribution.objects.filter(user_id=request.user).aggregate(Sum("amount"))["amount__sum"]
            total_loans = ApprovedLoan.objects.filter(user_id=request.user).aggregate(Sum("amount_left"))["amount_left__sum"]
            if not total_contributions:
                total_contributions = 0
            if not total_loans:
                total_loans = 0
            return render(request, "home.html", {"current_year": 2024, "union": union, 
                                                "total_contribution": total_contributions, 
                                                "total_loan_debt": total_loans})
        else:
            return render(request, "home.html", {"current_year": 2024})
    else:
        return render(request, "home.html", {"current_year": 2024})


@login_required
def add_member(request):
    # Add a field to take care of the date joined by the individual if they are a new member
    # If edited, then show the date edited
    """This function is used to add a new member to the database

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: Returns the webpage that is rendered
    """
    if request.method == "POST":
        """
        Checks if a member already exists in the database, if not adds them
        Returns a message if the member already exists
        """
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        msisdn = request.POST.get("phone").strip()
        if len(msisdn) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect("add_member")
        if not msisdn.isdigit():
            messages.error(request, "Phone number must be a number")
            return redirect("add_member")
        if msisdn[0] != "0":
            messages.error(request, "Phone number must start with 0")
            return redirect("add_member") 
        email = request.POST.get("email").strip()
        if not email:
            email = None
        dob = request.POST.get("dob")
        
        # amount = request.POST.get("amount")
        # if not amount:
        #     amount = 0
        all_members = [member.msisdn for member in Member.objects.all()]
        if email:
            check_email = KYCDetails.objects.filter(email=email).exists()
        else:
            check_email = False
        
        if int(msisdn) in all_members:
            messages.error(request, "Phone number already exists! Try with a different number")
            return redirect("add_member")
        
        if check_email:
            messages.error(request, "Email already exists! Try with a different email")
            return redirect("add_member")
    
        
        # if amount:
        #     if float(amount) < 0:
        #         messages.error(request, "The balance cannot be negative")
        #         return redirect("add_member")
        #     if not credit:
        #         CreditUnionBalance.objects.create(amount=amount)
        #     else:
        #         CreditUnionBalance.objects.update(amount=F("amount") + amount)
        #     member = Member.objects.create(msisdn=msisdn)
        #     KYCDetails.objects.create(member_msisdn=member, first_name=first_name, last_name=last_name, email=email, dob=dob)
        #     Contribution.objects.create(member_msisdn=member, amount=amount)
        #     Transaction.objects.create(member_msisdn=member, amount=amount, transaction_type=TransactionEnum.DEPOSIT, description="Initial deposit")
        user = request.user
        member = Member.objects.create(msisdn=msisdn, user_id=user)
        KYCDetails.objects.create(member_msisdn=member, first_name=first_name, last_name=last_name, email=email, dob=dob)
            
        return redirect("view_members")
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "add_member.html", {"current_year": 2024, "union": union})



# All filters will be done using the enums set in the models.py fio
@login_required
def view_members(request):
    # Create a filter for members
    sort = request.GET.get("sort", "first_name")
    order = request.GET.get("order", "")
    sorted = order + sort
    filter = request.GET.get("filter", MemberStatus.ACTIVE)
    
    members = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"),
                                        last_name=F("kycdetails__last_name"),
        total_contribution=Coalesce(Sum("contribution__amount", distinct=True), 0, output_field=DecimalField()),
        loan_debt=Coalesce(Sum("approvedloan__amount_left", distinct=True), 0, output_field=DecimalField())).order_by(sorted)
    
    if filter != "all":
        members = members.filter(status=filter).filter(user_id=request.user)
    
    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
  
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "view_members.html", {"current_year": 2024, "page_obj": page_obj, 
                                                 "sort":sort,
                                                 "order":order,
                                                 "filter":filter,
                                                 "union": union})


@login_required
def member_info(request, msisdn):
    member = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"), 
                                     last_name=F("kycdetails__last_name"), 
                                     total_contribution=Sum("contribution__amount"), 
                                     loan_debt=Sum("approvedloan__amount_left"), 
                                     email=F("kycdetails__email"), 
                                     dob=F("kycdetails__dob")).get(msisdn=msisdn)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "member.html", {"current_year": 2024, "member": member, "union": union})


@login_required
def edit_member(request, msisdn):
    member = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"), 
                                     last_name=F("kycdetails__last_name"), 
                                     email=F("kycdetails__email"), 
                                     dob=F("kycdetails__dob")
                                     ).get(msisdn=msisdn)
    
    if request.method == "POST":
        new_msisdn = int(request.POST.get("phone"))
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        member_obj = Member.objects.filter(user_id=request.user).get(msisdn=msisdn)
        member_obj.msisdn = new_msisdn
        member_obj.save()        
        kyc = get_object_or_404(KYCDetails, member_msisdn=member)
        kyc.email = email
        kyc.first_name = first_name
        kyc.last_name = last_name
        kyc.member_msisdn = member_obj 
        kyc.save()        
        return redirect("members", msisdn=new_msisdn)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "edit_member.html", {"current_year": 2024, "member": member, "union": union})


@login_required
def withdraw(request, msisdn):
    member = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"),
                                     last_name=F("kycdetails__last_name"),
                                     balance=ExpressionWrapper(Coalesce(Sum("contribution__amount", distinct=True), 0), DecimalField()),
                                     loan_debt=ExpressionWrapper(Coalesce(Sum("approvedloan__amount_left", distinct=True), 0), DecimalField()),
                                     interest=ExpressionWrapper(Coalesce(Sum("contribution__interest", distinct=True), 0), DecimalField()),
                                     final_balance=ExpressionWrapper(Coalesce(Sum("contribution__amount", distinct=True), 0) + 
                                                   Coalesce(Sum("contribution__interest", distinct=True), 0) - 
                                                   Coalesce(Sum("approvedloan__amount_left", distinct=True), 0), DecimalField())
                                     ).get(msisdn=msisdn)
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        if member.status == MemberStatus.INACTIVE:
            messages.error(request, f"{member.first_name} {member.last_name} is not an active member")
            return redirect("home")
        if date and time:
            pass
        elif date:
            time = datetime.now().time()
        elif time:
            date = datetime.now().date()
        else:
            time = datetime.now().time()
            date = datetime.now().date()
        credit_union_balance = CreditUnionBalance.objects.filter(user_id=request.user).first()
        if float(credit_union_balance.amount) < float(member.final_balance):
            messages.error(request, "The credit union balance is less than the total savings of the member cannot withdraw")
            messages.info(request, f"Credit union balance: {credit_union_balance.amount} Member savings: {member.final_balance}")
            return redirect("withdraw", msisdn=msisdn)
        if member.final_balance < 0:
            messages.error(request, "The member has a negative balance and cannot withdraw")
            return redirect("withdraw", msisdn=msisdn)
        credit_union_balance.amount = float(credit_union_balance.amount) - float(member.final_balance)
        
        credit_union_balance.save()
        if member.loan_debt > 0:
            
            Transaction.objects.create(member_msisdn=member, date=date, time=time, 
                                   transaction_type=TransactionEnum.LOAN_PAYMENT, 
                                   amount=member.loan_debt, 
                                   description="Payment of loan debt")        
        Transaction.objects.create(member_msisdn=member, date=date, time=time, 
                                   transaction_type=TransactionEnum.SAVINGS_WITHDRAWAL, 
                                   amount=member.final_balance, 
                                   description="Withdrawal of total savings")
        member.status = MemberStatus.INACTIVE
        member.save()
        return redirect("home")
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "withdraw.html", {"current_year": 2024, "member": member, "union": union})

# Contributions
@login_required
def make_contribution(request):
    # add ability to change the date when making a contribution
    members = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"), last_name=F("kycdetails__last_name"))
    if request.method == "POST":
        name = request.POST.get("member")
        amount = float(request.POST.get("amount"))
        date = request.POST.get("date")
        time = request.POST.get("time")
        interest = float(request.POST.get("interest"))/100
        interest = interest * amount
        if amount < 0:
            messages.error(request, "Amount cannot be negative")
            return redirect("make_contribution")
        one = name.split(" ")
        try:
            member = Member.objects.filter(user_id=request.user).get(kycdetails__first_name=one[0], kycdetails__last_name=one[1])
        except Member.DoesNotExist:
            messages.error(request, "Member not found")
            return redirect("make_contribution")
        Contribution.objects.create(member_msisdn=member, amount=amount, interest=interest, user_id=request.user)
        if date and time:
            pass
        elif date:
            time = datetime.now().time()
        elif time:
            date = datetime.now().date()
        else:
            time = datetime.now().time()
            date = datetime.now().date()
        Transaction.objects.create(member_msisdn=member, 
                                       transaction_type=TransactionEnum.DEPOSIT, 
                                       amount=amount, 
                                       description="Contribution",
                                       date=date,
                                       time=time)
        CreditUnionBalance.objects.update(amount=F("amount") + amount)
        messages.success(request, "Contribution made successfully")
        return redirect("view_members")
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "make_contribution.html", {"current_year": 2024, "members": members, "union": union})





# History
@login_required
def view_history(request):
    #Create a filter and sort the transactions
    sort = request.GET.get("sort", "transaction_created")
    order = request.GET.get("order", "-")
    sorted = order + sort
    filter = request.GET.get("filter", "all")
    members = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"), 
                                      last_name=F("kycdetails__last_name"), 
                                      transaction_type=F("transaction__transaction_type"),  
                                      description=F("transaction__description"), 
                                      amount=F("transaction__amount"),
                                      transaction_created=ExpressionWrapper(F("transaction__date") + F("transaction__time"), output_field=DateTimeField()),
                                      date = F("transaction__date")).filter(amount__gt=0).order_by(sorted)

    if filter != "all":
        members = members.filter(transaction_type=filter)
    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "history.html", {"current_year": 2024, "page_obj": page_obj,
                                            "sort":sort,
                                            "order":order,
                                            "filter":filter,
                                            "union": union})



# Loans
@login_required
def loan_request(request):
    sort = request.GET.get("sort", "loan_created")
    order = request.GET.get("order", "-")
    sorted = order + sort
    filter = request.GET.get("filter", "all")
    members = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"), 
                                      last_name=F("kycdetails__last_name"), 
                                      amount_requested=F("loanrequest__amount_requested"), 
                                      loan_status=F("loanrequest__status"), 
                                      date=F("loanrequest__request_date"), 
                                      loan_id=F("loanrequest__id"),
                                      loan_created=F("loanrequest__created")).filter(amount_requested__gt=0).order_by(sorted)
    if filter != "all":
        members = members.filter(loan_status=filter)

    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "loans_requests.html", {"current_year": 2024, "page_obj": page_obj,
                                          "sort":sort,
                                          "order":order,
                                          "filter":filter,
                                          "union":union})


@login_required
def approved_loans(request):
    sort = request.GET.get("sort", "updated")
    order = request.GET.get("order", "-")
    sorted = order + sort
    filter = request.GET.get("filter", "all")
    members = ApprovedLoan.objects.annotate(first_name=F("member_msisdn__kycdetails__first_name"), 
                                      last_name=F("member_msisdn__kycdetails__last_name"), 
                                      total_amount=F("amount_of_loan") + F("interest"),
                                      loan_id=F("loan_request_id"),
                                      ).filter(amount_of_loan__gt=0).order_by(sorted).filter(user_id=request.user)
    if filter != "all":
        members = members.filter(status=filter)

    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "loans.html", {"current_year": 2024, "page_obj": page_obj,
                                          "sort":sort,
                                          "order":order,
                                          "filter":filter,
                                          "union":union})

@login_required
def loan_details(request, loan_id):
    loan = LoanRequest.objects.annotate(first_name=F("member_msisdn__kycdetails__first_name"), 
                                        last_name=F("member_msisdn__kycdetails__last_name"), 
                                        loan_description=F("loan_purpose"),
                                        loan_status=F("status"), 
                                        date=F("request_date"), 
                                        loan_id=F("id")).get(id=loan_id)
    member = Member.objects.filter(user_id=request.user).get(msisdn=loan.member_msisdn.msisdn)
    year = datetime.now().year + 1
    month = datetime.now().month
    day = datetime.now().day
    due_date = datetime(year, month, day).date()
    try:
        approved = ApprovedLoan.objects.get(loan_request_id=loan)
        if approved.amount_left == 0 and approved.status != "PAID":
            approved.status = "PAID"
            approved.save()
        elif datetime.now().date() > approved.end_of_loan_date and approved.status != "PAID":
            approved.status = "OVERDUE"
            approved.save()
        if approved.status == "PAID":
            messages.success(request, "Loan has been paid")
        elif approved.status == "OVERDUE":
            messages.error(request, "Loan is overdue")

    except ApprovedLoan.DoesNotExist:
        approved = None
    
    
    if request.method == "POST":
        value = request.POST.get("button")
        if value == "approve":
            credit_union_balance = CreditUnionBalance.objects.filter(user_id=request.user).first()
            if credit_union_balance.amount <= loan.amount_requested:
                messages.error(request, "The amount being requested for loan is more than the available balance in the credit union!")
                messages.info(request, f"Amount available in the credit union: {credit_union_balance.amount} Amount being requested: {loan.amount_requested}")
                return redirect("loan_details", loan_id=loan_id)
            loan.status = LoanStatus.APPROVED
            loan.save()
            date = request.POST.get("date")
            time = request.POST.get("time")
            interest = float(request.POST.get("interest"))/100
            interest = interest * float(loan.amount_requested)
            amount_to_deduct = float(loan.amount_requested) + interest
            date_of_loan = request.POST.get("due_date")
            if date_of_loan:
                due_date = date_of_loan
            member = Member.objects.filter(user_id=request.user).get(msisdn=loan.member_msisdn.msisdn)
            if date and time:
                pass
            elif date:
                time = datetime.now().time()
            elif time:
                date = datetime.now().date()
            else:
                date = datetime.now().date()
                time = datetime.now().time()
            ApprovedLoan.objects.create(member_msisdn=member,
                                        loan_request_id=loan, 
                                        amount_of_loan=loan.amount_requested, 
                                        interest=interest, 
                                        end_of_loan_date=due_date,
                                        monthly_deduction=amount_to_deduct/12,
                                        amount_left=amount_to_deduct,
                                        user_id=request.user)
            credit_union_balance.amount = float(credit_union_balance.amount) - float(loan.amount_requested)
            credit_union_balance.save()
            Transaction.objects.create(member_msisdn=member, 
                                       transaction_type=TransactionEnum.LOAN_WITHDRAWAL, 
                                       amount=loan.amount_requested, 
                                       description=loan.loan_description,
                                       date=date,
                                       time=time)
            approved = ApprovedLoan.objects.filter(loan_request_id=loan)
            
            
        elif value == "reject":
            loan.status = "REJECTED"
            loan.save()
        return redirect("loan_details", loan_id=loan_id)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "loan_details.html", {"current_year": 2024, "loan": loan, "approved": approved, "due_date": due_date, "union": union})

@login_required
def input_loans(request):
    # Make it so the person can add his own date when making the loan request
    members = Member.objects.filter(user_id=request.user).annotate(first_name=F("kycdetails__first_name"), last_name=F("kycdetails__last_name"))
    if request.method == "POST":
        name = request.POST.get("member")
        amount = float(request.POST.get("loan_amount"))
        one = name.split(" ")
        if len(one) != 2:
            messages.error(request, "Please enter the first name and last name of the member")
            return redirect("input_loans")
        date = request.POST.get("date")
        time = request.POST.get("time")
        loan_purpose = request.POST.get("loan_purpose")
        if amount < 0:
            messages.error(request, "Loan amount cannot be negative")
            return redirect("input_loans")
        try:
            member = Member.objects.filter(user_id=request.user, status=MemberStatus.ACTIVE).get(kycdetails__first_name=one[0], kycdetails__last_name=one[1])
        except Member.DoesNotExist:
            messages.error(request, "Member not found")
            return redirect("input_loans")
        if date and time:
            pass
        elif date:
            time = datetime.now().time()
        elif time:
            date = datetime.now().date()
        else:
            time = datetime.now().time()
            date = datetime.now().date()
        LoanRequest.objects.create(member_msisdn=member, 
                                   amount_requested=amount, 
                                   loan_purpose=loan_purpose, 
                                   request_date=date, 
                                   request_time=time)

        return redirect("loan_request")
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "input_loans.html", {"current_year": 2024, "members": members, "union": union})


@login_required
def pay_loan(request, loan_id):
    loan = LoanRequest.objects.get(id=loan_id)
    approved = ApprovedLoan.objects.get(loan_request_id=loan)
    if request.method == "POST":
        amount_paid = float(request.POST.get("amount"))
        date = request.POST.get("date")
        time = request.POST.get("time")
        if amount_paid < 0:
            messages.error(request, "Amount paid cannot be negative")
            return redirect("pay_loan", loan_id=loan_id)
        approved = ApprovedLoan.objects.get(loan_request_id=loan_id)
        if amount_paid > approved.amount_left:
            messages.error(request, "The amount being paid is greater than what is left of the loan to be paid")
            messages.info(request, "Amount of loan left to be paid: GHc" + str(approved.amount_left) + ", Amount being paid: GHc" + str(amount_paid))

            return redirect("pay_loan", loan_id=loan_id)
        approved.amount_left = float(approved.amount_left) - amount_paid
        approved.save()
        if date and time:
            pass
        elif date:
            time = datetime.now().time()
        elif time:
            date = datetime.now().date()
        else:
            time = datetime.now().time()
            date = datetime.now().date()
        Transaction.objects.create(member_msisdn=loan.member_msisdn, 
                                       transaction_type=TransactionEnum.LOAN_PAYMENT, 
                                       amount=amount_paid, description="Loan payment", 
                                       date=date, time=time)
        credit_union_balance = CreditUnionBalance.objects.filter(user_id=request.user).first()
        credit_union_balance.amount = float(credit_union_balance.amount) + amount_paid
        credit_union_balance.save()
        return redirect("loan_details", loan_id=loan_id)
    union = CreditUnionBalance.objects.filter(user_id=request.user).first()
    return render(request, "pay_loan.html", {"current_year": 2024, "loan": loan, "union": union})