from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("add", views.add_member, name='add_member'),
    path("requests", views.input_loans, name='input_loans'),
    path("contribution", views.make_contribution, name='make_contribution'),
    path("members", views.view_members, name='view_members'),
    path("history", views.view_history, name='view_history'),
    path("loans", views.loan_request, name='loan_request'),
    path("members/<int:msisdn>", views.member_info, name='members'),
    path("members/<int:msisdn>/edit", views.edit_member, name='edit_member'),
    path("loans/<int:loan_id>", views.loan_details, name='loan_details'),
    path("loans/<int:loan_id>/pay", views.pay_loan, name='pay_loan'),
]