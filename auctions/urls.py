from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("article/mes_articles", views.vue_mes_articles, name="mes_articles"),
    path("article/articles_gagnés", views.vue_articles_gagnes, name="articles_gagnes"),
    path("article/favoris", views.vue_favoris, name="favoris"),
    path("article/creer", views.vue_creerArticle, name="creer"),
    path("article/categorie/<str:key_categorie>", views.vue_article, name="categorie"),
    path("article/<str:id_article>", views.index, name="visualiser"),
    path("watchlist", views.api_gestion_watchlist, name="api_watchlist"),
    path("enchere", views.api_gestion_enchere, name="api_enchere"),
    path("cloture", views.api_cloture_enchere, name="api_cloture"),
    path("commentaire", views.api_ajouter_commentaires, name="api_commentaire"),
    

]
