# Generated by Django 5.1.4 on 2025-01-13 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0022_remove_creditunionbalance_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loanrequest",
            name="request_time",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="time",
        ),
        migrations.AlterField(
            model_name="approvedloan",
            name="created",
            field=models.DateTimeField(),
        ),
    ]
