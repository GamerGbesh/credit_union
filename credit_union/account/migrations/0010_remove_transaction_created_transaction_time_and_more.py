# Generated by Django 5.1.4 on 2025-01-01 18:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0009_remove_kycdetails_id_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="created",
        ),
        migrations.AddField(
            model_name="transaction",
            name="time",
            field=models.TimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="member",
            name="status",
            field=models.CharField(
                choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")],
                default="ACTIVE",
                max_length=10,
            ),
        ),
    ]
