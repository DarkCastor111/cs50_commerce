from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    pass

class Bid(models.Model):
    pass

class AuctionListing(models.Model):
    CATEGORIES = {
        "MO" : "Mode",
        "JO" : "Jouets",
        "EL" : "Électronique",
        "MA" : "Maison",
    }
    titre = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    mise_a_prix = models.FloatField()
    categorie = models.CharField(max_length=64, choices=CATEGORIES, null=True)
    image_url = models.URLField(max_length=254, null=True)


