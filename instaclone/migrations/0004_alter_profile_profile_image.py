# Generated by Django 4.0.5 on 2022-06-10 11:00

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dz275mqsc/image/upload/v1654858776/default_nbsolf.png', max_length=255, verbose_name='image'),
        ),
    ]