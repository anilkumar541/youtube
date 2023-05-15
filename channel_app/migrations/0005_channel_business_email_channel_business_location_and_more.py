# Generated by Django 4.2 on 2023-05-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel_app', '0004_channel_channel_art'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='business_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='business_location',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='instagram',
            field=models.URLField(default='https://www.instagram.com'),
        ),
        migrations.AddField(
            model_name='channel',
            name='linkedin',
            field=models.URLField(default='https://www.linkedin.com'),
        ),
        migrations.AddField(
            model_name='channel',
            name='make_business_email_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='channel',
            name='make_business_location_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='channel',
            name='total_views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='channel',
            name='twitter',
            field=models.URLField(default='https://www.twitter.com'),
        ),
        migrations.AddField(
            model_name='channel',
            name='website',
            field=models.URLField(default='https://www.mywebsite.com'),
        ),
    ]
