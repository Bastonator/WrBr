# Generated by Django 4.2 on 2023-04-28 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stores', '0004_order_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='username',
        ),
    ]
