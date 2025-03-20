from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username} ({self.email})"



class AuctionListing(models.Model):
    CATEGORIES = {
        "--" : "Sans Catégorie",
        "MO" : "Mode",
        "JO" : "Jouets",
        "EL" : "Électronique",
        "MA" : "Maison"
    }
    titre = models.CharField(max_length=64)
    description = models.TextField()
    mise_a_prix = models.FloatField()
    categorie = models.CharField(max_length=64, choices=CATEGORIES, null=True)
    image_url = models.URLField(max_length=254, null=True)
    date_creation = models.DateTimeField()
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    actif = models.BooleanField()
    users_interesses=models.ManyToManyField(User, blank=True, related_name="watchlist")
    gagnant = models.ForeignKey(User, null = True, on_delete=models.CASCADE, related_name="articles_gagnes")

    def __str__(self):
        return f"{self.titre} : {self.categorie}"

class Bid(models.Model):
    date_creation = models.DateTimeField()
    valeur_enchere = models.FloatField()
    article = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="encheres")
    encherisseur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="encheres")

class Comment(models.Model):
    date_creation = models.DateTimeField()
    commentaire = models.TextField()
    article = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="commentaires")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentaires")


