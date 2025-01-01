# Generated by Django 5.1.4 on 2025-01-01 18:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0010_remove_transaction_created_transaction_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="loanrequest",
            name="request_time",
            field=models.TimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
