# Generated by Django 4.1 on 2023-08-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stores', '0031_alter_usercreatedpage_theme_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercreatedpage',
            name='theme_photo',
            field=models.ImageField(blank=True, default='images/no_image.jpg', null=True, upload_to=''),
        ),
    ]