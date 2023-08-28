from django.core.management.base import BaseCommand, CommandError
from pickle import load
from ...utils import PUNCTUATION
from recipes.models import *
from threading import Thread
import os

class Command(BaseCommand):
    help = 'Populate data from pickle files to database'

    def handle(self, *args, **options):
        
        recipes = load(open("pickle/recipes.pkl", 'rb'))
        utensils = load(open("pickle/utensils.pkl", 'rb'))
        ingredients = load(open("pickle/ingredients.pkl", 'rb'))
        # Hardcoding categories because these are all the categories
        # available in #marmiton
        categories = ["Apéritifs", "Entrées", "Plats", "Desserts", 
                    "Boissons", "Petit-déj/brunch"]
        threads = []
        

        def save_ingredient(name, image):
            Ingredient(name=name).save(img_url=image)

        def save_utensil(name, image):
            Utensil(name=name).save(img_url=image)

        print("Populating ingredients") 
        for name, image in ingredients.items():
            thread = Thread(target=save_ingredient, args=(name, image))
            thread.start()
            threads.append(thread)

        
        print("Populating utensils") 
        for name, image in utensils.items():
            thread = Thread(target=save_utensil, args=(name, image))
            thread.start()
            threads.append(thread)


        for thread in threads:
            thread.join()

        print("Ingredients populated successfully")
        print("Utensils populated successfully")

        if not os.path.exists('media/recipe_images'):
            os.mkdir('media/recipe_images')
        
        for recipe in recipes:
            try:
                recipe_obj = Recipe(title=recipe.title, description=recipe.description,
                            cost=recipe.cost, difficulty=recipe.difficulty,
                            preparation_time=recipe.prep_time, cooking_time=recipe.cook_time,
                            rest_time=recipe.rest_time, num_of_dishes=int(recipe.num_of_dishes))

                recipe_obj.save(ingr=recipe.ingredients, utns=recipe.utensils,
                                rcp=recipe)

                print(f"{recipe_obj} saved")
            except Exception as e:
                print('error occured', e)
        
        for category in categories:
            Category(name=category).save()

            print(f"{category} saved")


        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
