# Generated by Django 5.0.2 on 2024-02-11 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caregiver', '0008_alter_shift_managers_activity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='date',
            new_name='date_of_shift',
        ),
    ]
