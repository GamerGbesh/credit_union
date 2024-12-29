from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("add", views.add_member, name='add_member'),
    path("loans", views.input_loans, name='input_loans'),
    path("contribution", views.make_contribution, name='make_contribution'),
    path("members", views.view_members, name='view_members'),
    path("history", views.view_history, name='view_history'),

]