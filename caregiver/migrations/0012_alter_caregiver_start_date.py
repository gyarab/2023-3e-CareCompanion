# Generated by Django 5.0.2 on 2024-03-15 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caregiver', '0011_remove_caregiver_first_name_remove_caregiver_surname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='start_date',
            field=models.DateField(default='2024-01-01'),
        ),
    ]
