# Generated by Django 5.0.1 on 2024-01-20 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caregiver', '0005_caregiver_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='caregiver_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
