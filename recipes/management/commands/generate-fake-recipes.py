from django.utils.text import slugify
import random
from django.core.management.base import BaseCommand
from faker import Faker
import requests
from recipes.models import Ingredient, Utensil, Recipe, Category, RecipeImage, IngredientItem, UtensilItem
import os

class Command(BaseCommand):
    help = 'Generate fake data for database using Faker library'

    def handle(self, *args, **options):
        # Initialize Faker
        fake = Faker()
        
        # Ensure media directory exists
        os.makedirs('media/recipe_images', exist_ok=True)

        # Predefined categories
        categories = ["Appetizers", "Entrées", "Main Courses", "Desserts", "Drinks", "Breakfast/Brunch"]

        # Populate categories
        categories_images = os.listdir(os.path.join('resources'))
        category_objects = [Category(name=category, image=os.path.join('resources', 
                                                            random.choice(categories_images)),
                                    slug=slugify(category),
                                    )
                            for category in categories]
        print(category_objects, end='\n\n')
        
        Category.objects.bulk_create(category_objects)
        self.stdout.write(self.style.SUCCESS("Categories created successfully."))

        # Generate fake ingredients and utensils with random images
        ingredient_objects = []
        utensil_objects = []

        for _ in range(5):  # Generate 10 random ingredients and utensils
            ingredient_name = fake.word().capitalize()
            utensil_name = fake.word().capitalize()

            ingredient_objects.append(Ingredient(name=ingredient_name))
            utensil_objects.append(Utensil(name=utensil_name))

        Ingredient.objects.bulk_create(ingredient_objects)
        Utensil.objects.bulk_create(utensil_objects)
        self.stdout.write(self.style.SUCCESS("Ingredients and utensils populated successfully."))

        # Generate fake recipes
        for _ in range(10):  # Generate 10 random recipes
            recipe = Recipe(
                title=fake.sentence(nb_words=4),
                description=fake.text(),
                cost=fake.random_int(min=5, max=50),
                difficulty=fake.random_element(elements=('Easy', 'Medium', 'Hard')),
                preparation_time=f"{fake.random_int(min=0, max=23):02}:{fake.random_int(min=0, max=59):02}:{fake.random_int(min=0, max=59):02}",
                cooking_time=f"{fake.random_int(min=0, max=23):02}:{fake.random_int(min=0, max=59):02}:{fake.random_int(min=0, max=59):02}",
                rest_time=f"{fake.random_int(min=0, max=23):02}:{fake.random_int(min=0, max=59):02}:{fake.random_int(min=0, max=59):02}",
                num_of_dishes=fake.random_int(min=1, max=6),
            )
            recipe.save()

            images = os.listdir(os.path.join('resources', 'recipe'))
            recipeImage = RecipeImage(
                recipe=recipe,
                image = os.path.join('resources', 'recipe', random.choice(images))
                )
            recipeImage.save()

            # Assign random ingredients and utensils to each recipe
            recipe.ingredients.set(IngredientItem.objects.order_by('?')[:3])
            recipe.utensils.set(UtensilItem.objects.order_by('?')[:2])
            self.stdout.write(self.style.SUCCESS(f"Recipe '{recipe.title}' saved successfully."))

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully."))
