# Generated by Django 4.1 on 2023-10-29 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stores', '0036_alter_location_gambia_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location_gambia',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='location_gambia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
