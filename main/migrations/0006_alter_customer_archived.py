# Generated by Django 3.2.24 on 2024-04-15 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_product_producttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
