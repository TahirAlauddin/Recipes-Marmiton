"""The Purpose of this file is to set the images of the Recipes
that doesn't have an image attached to it. It reads the files in 
the folder resources/recipe and save the images to recipes."""
# Run this file in interactive console
import os
from django.core.files import File
from recipes.models import Recipe, RecipeImage  
from django.conf import settings

# Specify the folder containing the recipe images
image_folder = os.path.join(settings.BASE_DIR, 'resources', 'recipe')

# Retrieve all Recipe objects that don't have an associated RecipeImage
recipes_without_images = Recipe.objects.filter(recipe_images__isnull=True)

# Function to associate images with recipes
def assign_images_to_recipes():
    # List all files in the image folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    for recipe in recipes_without_images:

        if image_files:
            # Take the first image from the folder
            image_file = image_files[0]

            # Create a RecipeImage object and associate it with the recipe
            recipe_image = RecipeImage(recipe=recipe)
            
            # Open the image file and assign it to the RecipeImage object
            with open(os.path.join(image_folder, image_file), 'rb') as f:
                recipe_image.image.save(image_file, File(f), save=True)
            
            print(f"Assigned image '{image_file}' to '{recipe}'")

            # Remove the assigned image from the list
            image_files.pop(0)

# # Call the function to assign images to recipes
assign_images_to_recipes()
