from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os, os.path

# Get the User model, either Django's builtin User
# Or our Custom User, depending on the settings.py
User = get_user_model()

@login_required
def view_profile(request):
    return render(request, 'users/profile.html')


@login_required
def view_profile_update(request):
    # If POST request made, update the content of the profile
    if request.method == "POST":
        # Get the data form data
        form = request.POST
        username = form.get('username')
        email = form.get('email')
        birth_date = form.get('birth_date')
        address = form.get('address')
        postal_code = form.get('postal_code')
        city = form.get('city')
        country = form.get('country')
        gender = form.get('gender')
        profile_picture = request.FILES.get('profile_picture')

        # Update user attributes with the form data
        user = User.objects.get(id=request.user.id)
        if birth_date:
            user.birth_date = birth_date
        if address:
            user.address = address
        if postal_code:
            user.postal_code = postal_code
        if city:
            user.city = city
        if country:
            user.country = country
        if gender:
            user.gender = gender
        if profile_picture:
            user.profile.image = profile_picture
            user.profile.save()

        user.save()

        # Redirect the user to home page after 
        # successfully updating the profile
        return redirect('profile')
    return render(request, 'users/profile_update.html')
