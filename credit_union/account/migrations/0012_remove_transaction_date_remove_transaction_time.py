# Generated by Django 5.1.4 on 2025-01-01 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0011_loanrequest_request_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="date",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="time",
        ),
    ]
