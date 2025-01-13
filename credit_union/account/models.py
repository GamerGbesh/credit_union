from django.db import models

# Enum for member_status
class MemberStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'

# Enum for loan_status
class LoanStatus(models.TextChoices):
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    PENDING = 'PENDING', 'Pending'

# Enum for status_enum
class StatusEnum(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    PAID = 'PAID', 'Paid'
    OVERDUE = 'OVERDUE', 'Overdue'

# Enum for transaction_enum
class TransactionEnum(models.TextChoices):
    DEPOSIT = 'DEPOSIT', 'Deposit'
    SAVINGS_WITHDRAWAL = 'SAVINGS WITHDRAWAL', 'Savings Withdrawal'
    LOAN_PAYMENT = 'LOAN PAYMENT', 'Loan payment'
    LOAN_WITHDRAWAL = 'LOAN WITHDRAWAL', 'Loan Withdrawal'

class Member(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    msisdn = models.CharField(max_length=15, unique=True, primary_key=True)
    status = models.CharField(
        max_length=10,
        choices=MemberStatus.choices,
        default=MemberStatus.ACTIVE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class KYCDetails(models.Model):
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Contribution(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class LoanRequest(models.Model):
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=LoanStatus.choices, default=LoanStatus.PENDING)
    request_date = models.DateField()
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ApprovedLoan(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_request_id = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount_of_loan = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    end_of_loan_date = models.DateField()
    monthly_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=StatusEnum.choices, default=StatusEnum.ACTIVE)
    amount_left = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)



class CreditUnionBalance(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TransactionEnum.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    
