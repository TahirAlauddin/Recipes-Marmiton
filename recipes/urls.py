from django.urls import path
from . import views

urlpatterns = [
    path("create-recipe/", views.view_create_recipe, name="create-recipe"),
    path("create-ingredient/", views.view_create_ingredient, name="create-ingredient"),
    path("create-utensil/", views.view_create_utensil, name="create-utensil"),
    path("recipe/<str:slug>/", views.view_recipe_detail, name="recipe-detail"),
    path("approve-recipes/", views.view_non_approved_recipes, name='approve-recipes'),
    path("approve-recipes/<str:slug>", views.view_non_approved_recipes_detail, name='approve-recipes-detail'),
    path('', views.view_home, name='home'),

]