# Generated by Django 4.2.1 on 2023-06-18 10:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_rename_merchant_id_order_payment_intent"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="total_cost",
            new_name="paid_amount",
        ),
    ]
