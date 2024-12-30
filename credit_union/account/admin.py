from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Member)
admin.site.register(KYCDetails)
admin.site.register(Contribution)
admin.site.register(LoanRequest)
admin.site.register(ApprovedLoan)
# admin.site.register(MemberBalance)
admin.site.register(CreditUnionBalance)
admin.site.register(Transaction)
