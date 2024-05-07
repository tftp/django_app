# Generated by Django 3.2.24 on 2024-04-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20240419_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='auditory',
            field=models.CharField(max_length=4, verbose_name='Аудитория'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='house',
            field=models.CharField(max_length=3, verbose_name='Корпус'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='middlename',
            field=models.CharField(max_length=15, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=15, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='position',
            field=models.CharField(blank=True, max_length=30, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='start_job',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Поступил на работу'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='stop_job',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Уволился с работы'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='surname',
            field=models.CharField(max_length=15, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='telephone',
            field=models.CharField(max_length=4, verbose_name='Телефон'),
        ),
    ]
