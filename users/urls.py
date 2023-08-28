from django.urls import path
from .views import view_profile, view_profile_update

urlpatterns = [
    path('profile/', view_profile, name='profile'),
    path('profile-update/', view_profile_update, name='profile-update'),
]