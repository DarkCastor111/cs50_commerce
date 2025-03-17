from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, AuctionListing, Bid


def index(request):
    liste_articles = AuctionListing.objects.filter(actif=True)
    return render(request, "auctions/index.html", {
        "titre": "Tous les articles actifs",
        "articles_a_vendre": liste_articles,
        "nm_redirect" : "index"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        usn = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(request, username=usn, password=pwd)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        usn = request.POST["username"]
        mail = request.POST["email"]

        # Ensure password matches confirmation
        pwd = request.POST["password"]
        conf = request.POST["confirmation"]
        if pwd != conf:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(usn, mail, pwd)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def vue_creerArticle(request):
    if request.method == "POST":
        ttr = request.POST["form_titre"]
        desc = request.POST["form_desc"]
        map = request.POST["form_map"]
        cat = request.POST["form_cat"]
        img = request.POST["form_img"]
        # On crée un nouveau AuctionListing
        try:
            al = AuctionListing.objects.create(titre = ttr, 
                                               description = desc, 
                                               mise_a_prix = map, 
                                               categorie = cat, 
                                               image_url = img,
                                               proprietaire = request.user,
                                               date_creation = datetime.now(),
                                               actif = True)
            al.save()
        except (IntegrityError, ValueError):
            return render(request, "auctions/creer.html", {
                "message": "Erreur dans la creation de l'article.",
                "liste_categories": AuctionListing.CATEGORIES
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/creer.html", {
            "liste_categories": AuctionListing.CATEGORIES
        })

def vue_article(request, id_article):
    article_a_visualiser = AuctionListing.objects.get(pk=id_article)
    if article_a_visualiser:
        return render(request, "auctions/visualiser.html", {
            "article": article_a_visualiser,
            "categorie": AuctionListing.CATEGORIES.get(article_a_visualiser.categorie),
            "meilleure_enchere": article_a_visualiser.encheres.order_by('-valeur_enchere').first()
        })
    else:
        return render(request, "auctions/erreur.html", {
            "message": "Article non trouvé"
        })

def vue_mes_articles(request):
    liste_articles = request.user.articles.all()
    return render(request, "auctions/index.html", {
        "titre": "Mes articles",
        "articles_a_vendre": liste_articles,
        "nm_redirect": "mes_articles" 
    })

def vue_articles_gagnes(request):
    liste_articles = request.user.articles_gagnes.all()
    return render(request, "auctions/index.html", {
        "titre": "Articles gagnés",
        "articles_a_vendre": liste_articles,
        "nm_redirect": "articles_gagnes" 
    })


def vue_gestion_watchlist(request):
    # On ajoute le user à la liste des users_interesses de l'article
    id_article = request.POST["form_id_article"]
    mode = request.POST["form_mode"]
    redir = request.POST["form_redirect"]
    article = AuctionListing.objects.get(pk=id_article)
    usr = request.user
    if mode == "mode_ajout" : 
        article.users_interesses.add(usr)
    else:
        article.users_interesses.remove(usr)
    return HttpResponseRedirect(reverse(redir))

def vue_favoris(request):
    liste_articles = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
        "titre": "Favoris",
        "articles_a_vendre": liste_articles,
        "nm_redirect": "favoris" 
    })

def vue_gestion_enchere(request):
    id_article = request.POST["form_id_article"]
    art = AuctionListing.objects.get(pk=id_article)
    meilleure_enchere = art.encheres.order_by('-valeur_enchere').first()
    try:
        enchere = float(request.POST["form_enchere"])
    except ValueError:        
        return render(request, "auctions/visualiser.html", {
            "article": art,
            "categorie": AuctionListing.CATEGORIES.get(art.categorie),
            "message": "Enchère invalide.",
            "meilleure_enchere": meilleure_enchere
        }) 
    # Vérification d'une enchère valide
    if enchere <= art.mise_a_prix or (meilleure_enchere and enchere <= meilleure_enchere.valeur_enchere) :
        return render(request, "auctions/visualiser.html", {
            "article": art,
            "categorie": AuctionListing.CATEGORIES.get(art.categorie),
            "message": "Renseignez une meilleure enchère.",
            "meilleure_enchere": meilleure_enchere
        })        
    try:
        bi = Bid.objects.create(date_creation = datetime.now(),
                                valeur_enchere = enchere,
                                article = art,
                                encherisseur = request.user
                                )
        bi.save()
        art.users_interesses.add(request.user)
        art.mise_a_prix = enchere
        art.save()
    except (IntegrityError, ValueError):
        return render(request, "auctions/visualiser.html", {
            "article": art,
            "categorie": AuctionListing.CATEGORIES.get(art.categorie),
            "message": "Erreur BDD dans la creation de l'enchère.",
            "meilleure_enchere": art.encheres.order_by('-valeur_enchere').first()
        })
    return render(request, "auctions/visualiser.html", {
        "article": art,
        "categorie": AuctionListing.CATEGORIES.get(art.categorie),
        "meilleure_enchere": art.encheres.order_by('-valeur_enchere').first()
    })

def vue_cloture_enchere(request):
    id_article = request.POST["form_id_article"]
    art = AuctionListing.objects.get(pk=id_article)

    # Recherche de l'utilisateur gagnant l'enchère
    meilleure_enchere = art.encheres.order_by('-valeur_enchere').first()
    
    art.gagnant = meilleure_enchere.encherisseur
    art.actif = False
    art.save()

    return render(request, "auctions/visualiser.html", {
        "article": art,
        "categorie": AuctionListing.CATEGORIES.get(art.categorie),
        "message": "Enchère terminée.",
    })

    


