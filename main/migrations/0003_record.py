# Generated by Django 3.2.24 on 2024-04-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_date', models.DateField()),
                ('unset_date', models.DateField()),
            ],
        ),
    ]
