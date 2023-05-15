# Generated by Django 4.2 on 2023-05-11 05:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel_app', '0010_alter_channel_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='user_subs', to=settings.AUTH_USER_MODEL),
        ),
    ]
