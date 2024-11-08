from django.core.management.base import BaseCommand
from pickle import load, UnpicklingError
import json
import os
import re
from datetime import time, datetime

class Command(BaseCommand):
    help = 'Load data from pickle files and save in a readable format, with error handling for serialization issues.'

    def handle(self, *args, **options):
        data_summary = {
            "recipes": [],
            "utensils": [],
            "ingredients": []
        }

        json_file_path = 'resources/json/pickle_data.json'

        def clean_data(value):
            """Convert non-serializable data to a string format."""
            if isinstance(value, (time, datetime)):
                return value.strftime("%H:%M:%S")  # Format times as HH:MM:SS
            elif isinstance(value, (list, dict)):
                return value  # Nested data structures will be handled by json.dump
            elif isinstance(value, str):
                # Remove non-printable characters
                return re.sub(r'[^\x20-\x7E]+', ' ', value)
            else:
                return str(value)  # Fallback for any other data type

        try:
            # Attempt to load data from pickle files
            with open("pickle/recipes.pkl", 'rb') as f:
                try:
                    recipes = load(f)
                    for recipe in recipes:
                        recipe_info = {
                            "title": clean_data(getattr(recipe, 'title', 'N/A')),
                            "description": clean_data(getattr(recipe, 'description', 'N/A')),
                            "cost": clean_data(getattr(recipe, 'cost', 'N/A')),
                            "difficulty": clean_data(getattr(recipe, 'difficulty', 'N/A')),
                            "preparation_time": clean_data(getattr(recipe, 'prep_time', 'N/A')),
                            "cooking_time": clean_data(getattr(recipe, 'cook_time', 'N/A')),
                            "rest_time": clean_data(getattr(recipe, 'rest_time', 'N/A')),
                            "num_of_dishes": clean_data(getattr(recipe, 'num_of_dishes', 'N/A')),
                            "ingredients": [clean_data(str(ing)) for ing in getattr(recipe, 'ingredients', [])],
                            "utensils": [clean_data(str(ut)) for ut in getattr(recipe, 'utensils', [])]
                        }
                        data_summary["recipes"].append(recipe_info)
                except UnpicklingError:
                    self.stderr.write("Error: Could not load recipes pickle file.")

            with open("pickle/utensils.pkl", 'rb') as f:
                try:
                    utensils = load(f)
                    for name, image in utensils.items():
                        data_summary["utensils"].append({
                            "name": clean_data(name),
                            "image": clean_data(image)
                        })
                except UnpicklingError:
                    self.stderr.write("Error: Could not load utensils pickle file.")

            with open("pickle/ingredients.pkl", 'rb') as f:
                try:
                    ingredients = load(f)
                    for name, image in ingredients.items():
                        data_summary["ingredients"].append({
                            "name": clean_data(name),
                            "image": clean_data(image)
                        })
                except UnpicklingError:
                    self.stderr.write("Error: Could not load ingredients pickle file.")

            # Write data summary to log file in a readable JSON format
            with open(json_file_path, 'w') as log_file:
                json.dump(data_summary, log_file, indent=4, ensure_ascii=False)

            self.stdout.write(self.style.SUCCESS(f"Data successfully saved to {json_file_path}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to process pickle files: {e}"))
