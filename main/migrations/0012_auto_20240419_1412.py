# Generated by Django 3.2.24 on 2024-04-19 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20240418_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='start_job',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='stop_job',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='telephone',
            field=models.CharField(max_length=4),
        ),
    ]
