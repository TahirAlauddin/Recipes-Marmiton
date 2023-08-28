from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from threading import Thread
from dataclasses import dataclass
from typing import List, Any
from pickle import dump
from datetime import time
from django.core.management import BaseCommand
import requests
import os

url = 'https://marmiton.org'

SAVE_TO_PICKEL = True
PRINT_RESULTS = False
DEEPNESS = 20


scrapped = 0
skipped = 0
titles = []
threads = []
urls = []
utensil_names = []
ingredients_name_and_units = []
ingredients_names = []

# Database
ingredient_objects = []
utensil_objects = []
recipes_list = []


@dataclass
class Ingredient:
    name: str
    unit: str
    quantity: str
    image: str
    

@dataclass
class Utensil:
    name: str
    quantity: str
    image: str
    

@dataclass
class RecipeImage:
    image: bytes


@dataclass
class Recipe:
    title: str
    prep_time: Any
    rest_time: Any
    cook_time: Any
    difficulty: str
    cost: str
    description: str
    num_of_dishes: int
    ingredients: List[Ingredient]
    utensils: List[Utensil]
    recipe_image: RecipeImage


def str_to_time(prep_time, rest_time, cook_time):

    prep_time = prep_time.getText()
    rest_time = rest_time.getText()
    cook_time = cook_time.getText()

    if prep_time == '-':
        prep_time = time()
    else:
        prep_time_list = prep_time.split()
        num = prep_time_list[::2]
        unit = prep_time_list[1::2]

        minute = 0
        hour = 0
        for u, n in zip(unit, num):
            if u == 'hour':
                hour = n
            elif u == 'min':
                minute = n

        prep_time = time(hour=int(hour), minute=int(minute))
    
    if cook_time == '-':
        cook_time = time()
    else:
        cook_time_list = cook_time.split()
        num = cook_time_list[::2]
        unit = cook_time_list[1::2]

        minute = 0
        hour = 0
        for u, n in zip(unit, num):
            if u == 'hour':
                hour = n
            elif u == 'min':
                minute = n

        cook_time = time(hour=int(hour), minute=int(minute))

    if rest_time == '-':
        rest_time = time()
    else:
        rest_time_list = rest_time.split()
        num = rest_time_list[::2]
        unit = rest_time_list[1::2]

        minute = 0
        hour = 0
        for u, n in zip(unit, num):
            if u == 'hour':
                hour = n
            elif u == 'min':
                minute = n

        rest_time = time(hour=int(hour), minute=int(minute))
        
    return prep_time, rest_time, cook_time



def scrape_marmiton(url, deepness):
    global skipped, scrapped
    scrape = True

    if deepness >= DEEPNESS:
        return

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')

    # Call another recursive function as soon the response is get
    *_, random_recipe = soup.findAll('a', attrs={"class": "MRTN__sc-gkm9mr-3 jXEnlf"})
    href = random_recipe['href']

    if not href.startswith('http'):
        href = 'https://marmiton.org' + href 
    
    thread = Thread(target=scrape_marmiton, args=(href, deepness+1))
    thread.start()
    threads.append(thread)


    time,difficulty,cost = soup.findAll('p', attrs={'class': "RCP__sc-1qnswg8-1 iDYkZP"})


    #? Scrape picture of Recipe
    try:
        picture_of_recipe = soup.find('picture')
        picture_of_recipe = picture_of_recipe.find('source')

        picture_link = picture_of_recipe['srcset']
        picture_link = picture_link.split(',')[-1].split()[0]
        if not picture_link.startswith('http'):
            picture_link = url + picture_link

        response = requests.get(picture_link)
        recipe_picture_data = response.content
    except TypeError:
        # Picture not found
        with open('default_recipe.jpg', 'rb') as default_pic:
            recipe_picture_data = default_pic.read()

    #? Scrape Ingredients Picture
    ingredient_images = []
    pictures_of_ingredient = soup.findAll('div', attrs={'class': "RCP__sc-vgpd2s-2 fNmocT"})
    # picture_of_ingredient = picture_of_ingredient('picture', attrs={'class': ''})
    for picture_of_ingredient in pictures_of_ingredient:
        picture_of_ingredient = picture_of_ingredient.find('source')
        try:
            ingredient_picture_link = picture_of_ingredient['srcset']
            ingredient_picture_link = ingredient_picture_link.split(',')[-1].split()[0]
            if not ingredient_picture_link.startswith('http'):
                ingredient_picture_link = url + ingredient_picture_link

            print("Ingredient picture link:", ingredient_picture_link)

            ingredient_images.append(ingredient_picture_link)
        except TypeError:
            # Picture not found
            ingredient_images.append("default")


    #? Scrape Utensils Picture
    utensil_images = []
    pictures_of_utensil = soup.findAll('div', attrs={'class': "RCP__sc-1641h7i-5 fQNUFo"})
    # picture_of_utensil = picture_of_utensil('picture', attrs={'class': ''})
    for picture_of_utensil in pictures_of_utensil:
        picture_of_utensil = picture_of_utensil.find('source')

        try:
            utensil_picture_link = picture_of_utensil['srcset']
            utensil_picture_link = utensil_picture_link.split(',')[-1].split()[0]
            if not utensil_picture_link.startswith('http'):
                utensil_picture_link = url + utensil_picture_link

            print("Utensil picture link:", utensil_picture_link)
            utensil_images.append(utensil_picture_link)
        except TypeError:
            # Picture not found
            utensil_images.append("default")


    try:
        num_of_dishes = soup.find('span', attrs={'class': "SHRD__sc-w4kph7-4 hYSrSW"})
        num_of_dishes = num_of_dishes.getText()    
    except:
        num_of_dishes = 3

    description_and_steps = soup.find('ul', attrs={'class': None, 'id': None}).getText()
    time = time.getText(strip=True)
    total_time = time.split('\xa0')

    times = soup.findAll('span', attrs={'class': "SHRD__sc-10plygc-0 bzAHrL"})
    
    prep_time, rest_time, cook_time = times[1:]


    #? Converting string time to time object python
    prep_time, rest_time, cook_time = str_to_time(prep_time, rest_time, cook_time)

    #? Get the actual text from difficulty, cost and title_recipe in HTML
    difficulty = difficulty.getText()
    cost = cost.getText()
    title_recipe = soup.find('title').getText()


    ingredients_for_recipes = soup.findAll('span', attrs={"class": "SHRD__sc-10plygc-0 epviYI"})    
    ingredients_name_soup = soup.findAll('span', attrs={'class': "SHRD__sc-10plygc-0 kWuxfa"})
    utensils_soup = soup.findAll('div', attrs={"class": "RCP__sc-1641h7i-2 jUeCVL"})


    recipe_utensil_names = []
    recipe_ingredient_names = []


    # Adding ingredients to database if not exists
    for ingredient_name, ingredient_quantity_and_unit, ingredient_image in zip(ingredients_name_soup,
                                                         ingredients_for_recipes,
                                                         ingredient_images):
        ingredient_name = ingredient_name.getText(strip=True).strip()
        qty_unit_text = ingredient_quantity_and_unit.getText(strip=True).strip()


        quantity = ''.join([chr for chr in qty_unit_text if chr.isdigit() or chr == '/'])
        unit = ''.join([chr for chr in qty_unit_text if chr.isalpha()])

        recipe_ingredient_names.append(ingredient_name)

        if len(ingredient_name) > 20:
            skipped += 1
            scrape = False

        for i in ingredient_name:
            if i.isdigit():
                skipped += 1
                scrape = False
                break

        if ingredient_name not in ingredients_names:

            ingredient_object = Ingredient(name=ingredient_name, unit=unit, quantity=quantity,
                                            image=ingredient_image)
            ingredient_objects.append(ingredient_object)
            ingredients_names.append(ingredient_name)


    # Adding utensils to the database if not exists
    for utensil, utensil_image in zip(utensils_soup, utensil_images):
        # Utensils names 
        utensil_text = " ".join(utensil.getText().strip().split('\xa0'))
        utensil_name = "".join([chr for chr in utensil_text if chr.isalpha()])
        quantity = "".join([chr for chr in utensil_text if chr.isdigit()])

        recipe_utensil_names.append(utensil_name)
        if utensil_name not in utensil_names:
            utensil_object = Utensil(name=utensil_name, quantity=quantity,
                                    image=utensil_image)
            utensil_objects.append(utensil_object)
            utensil_names.append(utensil_name)

    recipe_ingredients = []
    recipe_utensils = []

    for ingredient_object in ingredient_objects:
        if ingredient_object.name in recipe_ingredient_names:
            recipe_ingredients.append(ingredient_object)


    for utensil_object in utensil_objects:
        if utensil_object.name in recipe_utensil_names:
            recipe_utensils.append(utensil_object)


    if difficulty.lower() == "très facile":
        difficulty = 'v'
    elif difficulty.lower() == "facile":
        difficulty = 'e'
    elif difficulty.lower() == "niveau moyen":
        difficulty = 'm'
    elif difficulty.lower() == "difficile":
        difficulty = 'h'

    if cost.lower() == 'bon marché':
        cost = 'c'
    elif cost.lower() in ['coût moyen', 'moyen']:
        cost = 'm'
    elif cost.lower() == 'assez cher':
        cost = 'e'

    if scrape:
        # Adding recipe to the database
        recipe = Recipe(title=title_recipe, prep_time=prep_time, cook_time=cook_time, 
                        rest_time=rest_time, difficulty=difficulty,
                        cost=cost, description=description_and_steps, 
                        ingredients=recipe_ingredients, utensils=recipe_utensils,
                        num_of_dishes=num_of_dishes, recipe_image=None)

        if recipe_picture_data:
            recipeImage = RecipeImage(image=recipe_picture_data)
            recipe.recipe_image = recipeImage


        recipes_list.append(recipe)
        titles.append(title_recipe)
        scrapped += 1
        print(f"{scrapped} Recipe added")



def print_results():
    print('\n\n\n\n')
    for ingredient_object in ingredient_objects:
        print(ingredient_object)

    print("\n\n")

    for utensil_object in utensil_objects:
        print(utensil_object)

    print("\n\n")

    for recipe in recipes_list:
        print(recipe)


class Command(BaseCommand):
    help = 'Scrapes recipe data from marmiton.org'

    def handle(self, *args, **options):
        
        main()
        ingredients = {}
        utensils = {}

        for ingredient_object in ingredient_objects:
            name = ingredient_object.name.lower()
            if name not in ingredients.keys():
                ingredients[name] = ingredient_object.image

        for utensil_object in utensil_objects:
            name = utensil_object.name
            if name not in utensils.keys():
                utensils[name] = utensil_object.image

        if not os.path.exists('pickle'):
            os.mkdir('pickle')


        # Save to pickel files
        # dump(recipes_list, open("pickle/recipes.pkl", 'wb'))
        # dump(ingredients, open("pickle/ingredients.pkl", 'wb'))
        # dump(utensils, open("pickle/utensils.pkl", 'wb'))


        self.stdout.write(self.style.SUCCESS("Recipes scrapped successfully."))


# Program Start from here
def main():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')

    recipes = soup.findAll('div', attrs={"class":"m_contenu_bloc"})

    for recipe in recipes:
        result = recipe.findParent('a')
        try:
            href = result['href']
            if href.endswith('html'):
                continue

            if not href.startswith('http'):
                href = 'https://marmiton.org' + href 

            thread = Thread(target=scrape_marmiton, args=(href,0))
            thread.start()
            threads.append(thread)

        except TypeError:
            pass


    for thread in threads:
        thread.join()

    print(skipped)
    print("Scrapped", scrapped)


if __name__ == '__main__':
    main()
