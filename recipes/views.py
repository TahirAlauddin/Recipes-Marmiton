from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages 
from django.http import JsonResponse
from django.conf import settings
from miscellenous.models import *
from .models import *
from .utils import *
from datetime import time

# Helper functions and Variables
User = get_user_model()

# A wrapper function to be used on top of a decorator
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


# Home Page/ Recipe List Page
def view_home(request):
    recipes = Recipe.objects.filter(approved=True).order_by('?')[:10]
    context = {'recipes': recipes}
    return render(request, "recipes/index.html", context)


# Login required decorator used so only authenticated users can get
# access to this endpoint
@login_required
def view_create_recipe(request):
    if request.method == 'POST':
        # Let the utility/helper function do its job
        # It takes request object and returns True if 
        # all necessary IngredientItems,UtensilItems,
        # Recipe and RecipeImages were created successfully
        recipe = handle_recipe_creation(request)

        if recipe:
            messages.add_message(request, level=messages.SUCCESS, message=RECIPE_CREATED_SUCCESS_MESSAGE)
        # Redirect the user to the detail page of the recipe just created
        return redirect('recipe-detail', recipe.slug)
    
    # Retrieve all ingredients, utensils and categories to
    # show as a choice field in the html template
    ingredients = Ingredient.objects.filter(approved=True)
    utensils = Utensil.objects.all()
    categories = Category.objects.all()
    units = [unit_name for unit, unit_name in UNITS]
    # Create a context dictionary and pass it to the template
    context = {'ingredients': ingredients, 'utensils': utensils,
                'categories': categories, 'units': units}
                
    return render(request, "recipes/add_recipe.html", context=context)


# Login required decorator used so only authenticated users can get
# access to this endpoint
@login_required
def view_create_ingredient(request):
    if request.method == "POST":
        form = request.POST
        # Create a new ingredient
        Ingredient(name = form.get('name'),
                   image = request.FILES.get('image')).save()
        
        messages.add_message(request, level=messages.SUCCESS, message=INGREDIENT_CREATED_SUCCESS_MESSAGE)
        return redirect('home')

    return render(request, "recipes/add_ingredients.html")


# Login required decorator used so only authenticated users can get
# access to this endpoint
@login_required
def view_create_utensil(request):
    if request.method == "POST":
        form = request.POST

        # Create a new ingredient
        Utensil(name = form.get('name'),
                image = request.FILES.get('image')).save()        

        # Let the user know that the utensil was created successfully
        messages.add_message(request, level=messages.SUCCESS, message=UTENSIL_CREATED_SUCCESS_MESSAGE)
        return redirect('home')
        
    return render(request, "recipes/add_utensils.html")


# Use slug as a unique identifier of a recipe in the website
def view_recipe_detail(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    if request.method == "POST":
        # A review was left because http request method is POST
        form = request.POST
        user = request.user
        if isinstance(user, User):
            # Same user can't give more than 1 reviews to a single recipe
            reviews = Review.objects.filter(owner=user, recipe=recipe)
            if reviews:
                messages.add_message(request, level=messages.WARNING,
                message=USER_ALREADY_GIVEN_REVIEW)
            else:
                messages.add_message(request, level=messages.SUCCESS,
                message=THANKS_FOR_REVIEW)

                Review(recipe=recipe, rating=form.get('rating'),
                        content=form.get('content'), owner=user).save()
            return redirect('recipe-detail', slug)
        else:
            return redirect('account_login')
    # Get all ingredientItems and utensilItems related the current
    # recipe, Create a context and pass it to the template
    ingredients = recipe.ingredients.all()
    utensils = recipe.utensils.all()
    reviews = recipe.reviews.all()
    # Create a range object/iterator to help render exactly 
    # the number of stars as rating as recipe.average_rating 
    rating_count = range(int(recipe.average_rating))
    images = recipe.recipe_images.all()
    if images:
        images = images[1:]
        
    images_length_iterator = range(len(images))
    context = {'recipe': recipe, 'ingredientItems': ingredients, 
                'utensilItems': utensils, 'comments': reviews,
                'rating_count': rating_count, 'images': images,
                'images_length_iterator': images_length_iterator} 
    return render(request, "recipes/recipe_detail.html", context=context)


# API view created for +, - functionality in Recipe detail page
# Takes the slug of the recipe and number of dishes and returns
# a list of ingredient quantities for that particular number of dishes
def get_ingredients_quantity_api_view(request, slug, current_num_of_dishes):
    recipe = Recipe.objects.get(slug=slug)
    quantities = recipe.get_quantity_of_ingredients_from_number_of_dishes(current_num_of_dishes)
    return JsonResponse(quantities, safe=False)


# Only authenticated users who are also staff members can access to this page
# This is an admin page where staff members can approve a recipe
@login_required
@staff_required(login_url=settings.LOGIN_URL)
def view_non_approved_recipes(request):
    un_approved_recipes = Recipe.objects.filter(approved=False)
    context = {'recipes': un_approved_recipes}
    return render(request, 'recipes/unapproved_recipes.html', context=context)


@login_required
@staff_required(login_url=settings.LOGIN_URL)
def view_non_approved_recipes_detail(request, slug):
    un_approved_recipe = Recipe.objects.get(slug=slug)
    if request.method == "POST":
        # Approve it
        un_approved_recipe.approved = True
        un_approved_recipe.save()
        return redirect('approve-recipes')
    # Get all ingredientItems and utensilItems related the current
    # recipe, Create a context and pass it to the template
    ingredients = un_approved_recipe.ingredients.all()
    utensils = un_approved_recipe.utensils.all()

    images = un_approved_recipe.recipe_images.all()
    # If there are images related to a recipe
    # then exclude the first image in the queryset 
    # because it will be automatically included
    # in recipe.thumbnail_image property method.
    if images:
        images = images[1:]

    context = {'recipe': un_approved_recipe, 'images': images,
                'ingredientItems': ingredients, 'utensilItems': utensils}
    return render(request, 'recipes/unapproved_recipes_detail.html', context=context)
