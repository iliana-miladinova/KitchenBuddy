# Generated by Django 5.1.4 on 2025-02-14 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0003_remove_substitute_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('fruits', 'Fruits'), ('vegetables', 'Vegetables'), ('dairy', 'Dairy'), ('meat', 'Meat'), ('grains', 'Grains'), ('spices', 'Spieces'), ('fish', 'Fish'), ('nuts', 'Nuts'), ('other', 'Other')], max_length=20),
        ),
    ]
