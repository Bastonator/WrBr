# Generated by Django 4.1 on 2023-11-07 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stores', '0036_location_gambia_wellingara'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercreatedpage',
            name='id',
            field=models.CharField(default='to-be-named', max_length=155, primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
    ]