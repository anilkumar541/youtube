# Generated by Django 4.2 on 2023-04-28 06:25

import channel_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel_app', '0003_channel_verified_alter_channel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_art',
            field=models.ImageField(blank=True, null=True, upload_to=channel_app.models.user_directory_path),
        ),
    ]
