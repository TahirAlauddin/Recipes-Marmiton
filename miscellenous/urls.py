from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_category, name='category'),
    path("<str:slug>/", views.view_category_detail, name='category-detail'),
]
