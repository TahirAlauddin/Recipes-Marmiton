from .models import *
import string


#####! CONSTANTS/VARIABLES #####

#? USED IN VIEWS
RECIPE_CREATED_SUCCESS_MESSAGE = "Recipe created successfully! Admins will approve it and then the recipe will be public"
INGREDIENT_CREATED_SUCCESS_MESSAGE = "Ingredient created successfully! Admins will approve it and then the ingredient will be public"
UTENSIL_CREATED_SUCCESS_MESSAGE = "Utensil created successfully!"
USER_ALREADY_GIVEN_REVIEW = "Oops! It looks like you have already given a review to this recipe.\
                            You can't give more than exactly 1 review."
THANKS_FOR_REVIEW = "Thanks for sharing your feedback!"


#? USED IN MODELS
PUNCTUATION = string.punctuation
UNITS = [
    # Volume
    ("tsp", "teaspoon"),
    ("tbsp", "tablespoon"),
    ("c", "cup"),
    ("pt", "pint"),
    ("qt", "quart"),
    ("gal", "gallon"),
    ("ml", "milliliter"), 
    ("l", "liter"), 
    ("dl", "deciliter"),
    ("fl oz", "fluid ounce"),

    # Mass and Weight
    ("lb", "pound"),
    ("oz", "ounce"),
    ("mg", "milligram"),
    ("g", "gram"),
    ("kg", "kilogram"),

    # Length
    ("mm", "millimeter"),
    ("cm", "centimeter"),
    ("m", "meter"),
    ("in", "inch"),
]


DIFFICULTY_CHOICES = [
    ('v', 'Very Easy'),
    ('e', 'Easy'),
    ('m', 'Medium'),
    ('h', 'Hard'),
]

COST_CHOICES =  [
    ('c', 'Cheap'),
    ('m', 'Medium'),
    ('e', 'Expensive'),
]


#####! FUNCTIONS #####

#? USED IN 
def handle_recipe_creation(request):
    form = request.POST
    images = request.FILES.getlist('images')

    ingredients_quantity = form.getlist('ingredients-quantity')
    ingredients_name = form.getlist('ingredients-name')
    ingredients_unit = form.getlist('ingredients-unit')
    utensils_quantity = form.getlist('utensils-quantity')
    utensils_name = form.getlist('utensils-name')

    category_name = form.get('category')
    cost = form.get('cost')
    difficulty = form.get('difficulty')
    video_url=form.get('video-url')
    
    # Write corresponding character into database
    # v for Very Easy, e for easy and so on
    for diff in DIFFICULTY_CHOICES:
        if diff[1] == difficulty:
            difficulty = diff[0]

    # Write corresponding character into database
    # c for Cheap, m for medium and so on
    for cost_choice in COST_CHOICES:
        if cost_choice[1] == cost:
            cost = cost_choice[0]


    category = Category.objects.filter(name=category_name)
    
    # Create a recipe object with form data
    recipe = Recipe(title=form.get('title'), description=form.get('description'),

                    cost=cost, difficulty=difficulty,

                    preparation_time=time(hour=int(form.get('prep-hours')),
                                        minute=int(form.get('prep-minutes'))),
                    cooking_time=time(hour=int(form.get('cooking-hours')),
                                        minute=int(form.get('cooking-minutes'))),
                    rest_time = time(hour=int(form.get('rest-hours')),
                                        minute=int(form.get('rest-minutes'))),

                    num_of_dishes=form.get('dishes'), 
                    )
    if category:
        category = category[0]
        recipe.category = category
    if video_url:
        recipe.video_url = video_url

    if not recipe.save():
        return recipe

    # Add images to the recipe
    for image in images:
        RecipeImage(image=image, recipe=recipe).save()

    for ingredient_name, ingredient_unit, ingredient_quantity in zip(ingredients_name, ingredients_unit, ingredients_quantity):
        # Create a IngredientItem object and save it to the database

        ingredient = Ingredient.objects.get(name=ingredient_name)
        IngredientItem(ingredient=ingredient, quantity=ingredient_quantity,
                        unit=ingredient_unit, recipe=recipe).save()

    for utensil_name, utensil_quantity in zip(utensils_name, utensils_quantity):
        # Create a UtensilItem object and save it to the database

        utensil = Utensil.objects.get(name=utensil_name)
        UtensilItem(utensil=utensil, quantity=utensil_quantity,
                                        recipe=recipe).save()

    return recipe