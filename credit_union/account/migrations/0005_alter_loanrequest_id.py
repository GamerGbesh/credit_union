# Generated by Django 5.1.4 on 2024-12-30 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_alter_loanrequest_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loanrequest",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
