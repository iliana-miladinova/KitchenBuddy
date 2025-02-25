# Generated by Django 5.1.4 on 2025-02-12 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Substitute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='ingredients.ingredient')),
                ('substitute_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substitude_ingrdient', to='ingredients.ingredient')),
            ],
            options={
                'ordering': ['ingredient__name', 'substitute_ingredient__name'],
            },
        ),
    ]
