# Generated by Django 5.1.6 on 2025-03-13 21:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctionlisting_actif'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='users_interesses',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
