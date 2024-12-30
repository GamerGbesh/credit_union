# Generated by Django 5.1.4 on 2024-12-30 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="loanrequest",
            name="loan_purpose",
            field=models.CharField(default="loan request", max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="creditunionbalance",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="loanrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("APPROVED", "Approved"),
                    ("REJECTED", "Rejected"),
                    ("PENDING", "Pending"),
                ],
                default="PENDING",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="memberbalance",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
