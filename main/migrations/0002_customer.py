# Generated by Django 3.2.24 on 2024-04-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('surname', models.CharField(max_length=15)),
                ('middlename', models.CharField(max_length=15)),
                ('position', models.CharField(max_length=30)),
                ('house', models.CharField(max_length=3)),
                ('auditory', models.CharField(max_length=4)),
                ('telephone', models.CharField(max_length=11)),
                ('archived', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
