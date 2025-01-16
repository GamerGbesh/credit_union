from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("add", views.add_member, name='add_member'),
    path("requests", views.input_loans, name='input_loans'),
    path("contribution", views.make_contribution, name='make_contribution'),
    path("member", views.view_members, name='view_members'),
    path("history", views.view_history, name='view_history'),
    path("loan_request", views.loan_request, name='loan_request'),
    path("loans", views.approved_loans, name='view_loans'),
    path("member/<str:msisdn>", views.member_info, name='members'),
    path("member/<str:msisdn>/edit", views.edit_member, name='edit_member'),
    path("member/<str:msisdn>/withdraw", views.withdraw, name='withdraw'),
    path("member/<str:msisdn>/delete", views.delete, name="delete"),
    path("loans/<int:loan_id>", views.loan_details, name='loan_details'),
    path("loans/<int:loan_id>/pay", views.pay_loan, name='pay_loan'),
    path('download-contribution/', views.contributions_to_excel, name='download_contribution'),
    path('download-requests/', views.requests_to_excel, name='download_requests'),
    path('download-history/', views.history_to_excel, name='download_history'),
    path('download-loans/', views.loans_to_excel, name='download_loans'),
    path("choice", views.choice, name="member_choice"),
    path("loan_choice", views.loan_choice, name="loan_choice"),
]