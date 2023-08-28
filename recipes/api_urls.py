from django.urls import path
from .views import get_ingredients_quantity_api_view

urlpatterns = [
    path('get_num_of_dishes/<str:slug>/<int:current_num_of_dishes>/',
        get_ingredients_quantity_api_view, name='ingredients-quantity')
]