# Generated by Django 5.1.6 on 2025-03-19 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_commentaire_comment_commentaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_creation',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_creation',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_creation',
            field=models.DateTimeField(),
        ),
    ]
