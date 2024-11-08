from django.core.management.base import BaseCommand
from faker import Faker
import requests
from recipes.models import Ingredient, Utensil, Recipe, Category
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
        category_objects = [Category(name=category) for category in categories]
        Category.objects.bulk_create(category_objects)
        self.stdout.write(self.style.SUCCESS("Categories created successfully."))

        # Generate fake ingredients and utensils with random images
        ingredient_objects = []
        utensil_objects = []

        for _ in range(10):  # Generate 10 random ingredients and utensils
            ingredient_name = fake.word().capitalize()
            utensil_name = fake.word().capitalize()

            # Get random images from an API like Lorem Picsum
            ingredient_image_url = f"https://picsum.photos/200/200?random={fake.random_number()}"
            utensil_image_url = f"https://picsum.photos/200/200?random={fake.random_number()}"

            # Save images locally
            ingredient_image_path = f'media/recipe_images/{ingredient_name}.jpg'
            utensil_image_path = f'media/recipe_images/{utensil_name}.jpg'

            with open(ingredient_image_path, 'wb') as img_file:
                img_file.write(requests.get(ingredient_image_url).content)
            with open(utensil_image_path, 'wb') as img_file:
                img_file.write(requests.get(utensil_image_url).content)

            ingredient_objects.append(Ingredient(name=ingredient_name, image=ingredient_image_path))
            utensil_objects.append(Utensil(name=utensil_name, image=utensil_image_path))

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
                preparation_time=fake.random_int(min=5, max=60),
                cooking_time=fake.random_int(min=5, max=60),
                rest_time=fake.random_int(min=0, max=30),
                num_of_dishes=fake.random_int(min=1, max=6),
            )
            recipe.save()

            # Assign random ingredients and utensils to each recipe
            recipe.ingredients.set(Ingredient.objects.order_by('?')[:3])
            recipe.utensils.set(Utensil.objects.order_by('?')[:2])
            self.stdout.write(self.style.SUCCESS(f"Recipe '{recipe.title}' saved successfully."))

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully."))
