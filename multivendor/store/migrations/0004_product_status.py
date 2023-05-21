# Generated by Django 4.2.1 on 2023-05-21 00:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_alter_product_options_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("waiting_for_approval", "Waiting for approval"),
                    ("active", "Active"),
                    ("deleted", "Deleted"),
                ],
                default="active",
                max_length=50,
            ),
        ),
    ]
