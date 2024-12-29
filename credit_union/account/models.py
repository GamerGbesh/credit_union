from django.db import models

# Enum for member_status
class MemberStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    SUSPENDED = 'SUSPENDED', 'Suspended'

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
    SAVINGS_WITHDRAWAL = 'SAVINGS_WITHDRAWAL', 'Savings Withdrawal'
    LOAN_REPAYMENT = 'LOAN_REPAYMENT', 'Loan Repayment'
    LOAN_WITHDRAWAL = 'LOAN_WITHDRAWAL', 'Loan Withdrawal'

class Member(models.Model):
    msisdn = models.IntegerField(primary_key=True)
    deleted = models.BooleanField(default=False)
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
    id_type = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Contribution(models.Model):
    id = models.AutoField(primary_key=True)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class LoanRequest(models.Model):
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=LoanStatus.choices, default=LoanStatus.PENDING)
    request_date = models.DateField(auto_now_add=True)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ApprovedLoan(models.Model):
    id = models.AutoField(primary_key=True)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount_of_loan = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    end_of_loan_date = models.DateField()
    monthly_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=StatusEnum.choices)
    amount_left = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class MemberBalance(models.Model):
    id = models.AutoField(primary_key=True)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class CreditUnionBalance(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    member_msisdn = models.ForeignKey(Member, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TransactionEnum.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
