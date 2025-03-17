from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("article/mes_articles", views.vue_mes_articles, name="mes_articles"),
    path("article/favoris", views.vue_favoris, name="favoris"),
    path("article/creer", views.vue_creerArticle, name="creer"),
    path("article/<str:id_article>", views.vue_article, name="visualiser"),
    path("watchlist", views.vue_gestion_watchlist, name="api_watchlist"),
    path("enchere", views.vue_gestion_enchere, name="api_enchere"),
    

]
