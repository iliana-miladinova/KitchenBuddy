# Generated by Django 5.1.4 on 2025-02-15 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_profile_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activity',
            field=models.CharField(blank=True, choices=[('sedentary', 'sedentary'), ('light', 'light active'), ('moderate', 'moderate active'), ('very', 'very active')], max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6),
        ),
    ]
