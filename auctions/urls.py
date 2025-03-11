from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("article/creer", views.vue_creerArticle, name="creer"),
    path("article/<str:id_article>", views.vue_article, name="visualiser"),
    

]
