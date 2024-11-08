from django.core.management.base import BaseCommand, CommandError
import json
import os
from recipes.models import Ingredient, Utensil, Recipe, Category

class Command(BaseCommand):
    help = 'Populate database from JSON data log file'

    def add_arguments(self, parser):
        # Allow the user to specify the JSON file path
        parser.add_argument(
            '--file',
            type=str,
            default='resources/json/pickle_data.json',
            help='Path to the JSON file containing data'
        )

    def handle(self, *args, **options):
        # Get the JSON file path from command arguments
        file_path = options['file']

        # Check if the JSON file exists
        if not os.path.exists(file_path):
            raise CommandError(f"File {file_path} does not exist. Please check the path and try again.")

        # Load data from JSON file
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise CommandError(f"Error decoding JSON file: {e}")

        # Create or get categories
        categories = ["Appetizers", "Entrées", "Main Courses", "Desserts", "Drinks", "Breakfast/Brunch"]
        category_objects = {name: Category.objects.get_or_create(name=name)[0] for name in categories}

        # Populate Ingredients
        if "ingredients" in data:
            ingredient_objects = []
            for ingredient in data["ingredients"]:
                name = ingredient.get("name")
                image = ingredient.get("image")
                if name:
                    ingredient_objects.append(Ingredient(name=name, image=image))
            Ingredient.objects.bulk_create(ingredient_objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"{len(ingredient_objects)} ingredients populated successfully."))

        # Populate Utensils
        if "utensils" in data:
            utensil_objects = []
            for utensil in data["utensils"]:
                name = utensil.get("name")
                image = utensil.get("image")
                if name:
                    utensil_objects.append(Utensil(name=name, image=image))
            Utensil.objects.bulk_create(utensil_objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"{len(utensil_objects)} utensils populated successfully."))

        # Populate Recipes
        if "recipes" in data:
            for recipe in data["recipes"]:
                try:
                    recipe_obj = Recipe(
                        title=recipe.get("title", "No Title"),
                        description=recipe.get("description", ""),
                        cost=recipe.get("cost", ""),
                        difficulty=recipe.get("difficulty", ""),
                        preparation_time=recipe.get("preparation_time", "00:00:00"),
                        cooking_time=recipe.get("cooking_time", "00:00:00"),
                        rest_time=recipe.get("rest_time", "00:00:00"),
                        num_of_dishes=int(recipe.get("num_of_dishes", 1))
                    )
                    recipe_obj.save()

                    # Set ingredients and utensils
                    ingredient_names = recipe.get("ingredients", [])
                    utensil_names = recipe.get("utensils", [])

                    # Retrieve ingredients and utensils by name
                    ingredients = Ingredient.objects.filter(name__in=ingredient_names)
                    utensils = Utensil.objects.filter(name__in=utensil_names)

                    recipe_obj.ingredients.set(ingredients)
                    recipe_obj.utensils.set(utensils)

                    self.stdout.write(self.style.SUCCESS(f"Recipe '{recipe_obj.title}' saved successfully."))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error saving recipe '{recipe.get('title', 'Unknown')}': {e}"))

        self.stdout.write(self.style.SUCCESS("Database populated successfully from JSON data."))
