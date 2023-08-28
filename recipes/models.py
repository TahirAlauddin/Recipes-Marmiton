from django.db import models
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.conf import settings
from django.db.utils import IntegrityError
from datetime import time, timedelta
from miscellenous.models import Category
from .utils import *
import os, urllib.request



class Ingredient(models.Model):
    """"
    An Ingredient of a product, a recipe in this case.
    There is a Many to Many Relationship between Recipe and
    Ingredient. Hence, there can be many Ingredients belonging 
    to a single Recipe and also many Recipes pointing to same
    Ingredient.
    - name: The name of the Ingredient i.e. Tomato, Water etc.
    - approved: Whether the Ingredient is approved or not
    """
    name = models.CharField(max_length=120, 
                            unique=True,
                            help_text="Maximum 120 characters",
                            )
    image = models.ImageField(upload_to='ingredients',
                                default='default_ingredient.jpg')
    approved = models.BooleanField(null=False, default=False)


    def save(self, *args, **kwargs):
        """ Overriding save method of models.Model to save
        the images from #marmiton for each ingredient using
        the url scrapped in scrape-recipes command """
        
        try:
            img_url = kwargs.pop('img_url')
        except KeyError:
            return

        image_filename = self.name.translate(str.maketrans('', '', PUNCTUATION)) + '.jpg'
        try:            
            # image_url is a URL to the image which #marmiton is using
            result = urllib.request.urlretrieve(img_url) 
        except:
            return

        # self.photo is the ImageField
        self.image.save(
            os.path.join(image_filename),
            File(open(result[0], 'rb'))
            )
            
        super(Ingredient, self).save(*args, **kwargs)
        

    def __str__(self):
        """ String Representation of the object of Ingredient """
        return self.name

    class Meta:
        """ Meta Configurations of the class Ingredient """
        # The order in which ingredients show on admin panel
        ordering = ['name'] 
        # The name which shows on the admin page
        verbose_name = _('Ingredient')
        # The plural name which shows on the admin page
        verbose_name_plural = _('Ingredients')


class Utensil(models.Model):
    """"
    A utensil which is need to cook/make/bake a recipe or a product.
    There is a Many to Many Relationship between Recipe and
    Utensil. Hence, there can be many Utensils belonging 
    to a single Recipe and also many Recipes pointing to same
    Utensil.
    - name: The name of the Utensil i.e. Plates, Spoon etc.
    """
    name = models.CharField(max_length=120, 
                            unique=True,
                            help_text="Maximum 120 characters",
                            )
    image = models.ImageField(upload_to='utensils',
                                default='default_utensil.jpg')

    def save(self, *args, **kwargs):
        """ Overriding save method of models.Model to save
        the images from #marmiton for each utensil using
        the url scrapped in scrape-recipes command """
        try:
            img_url = kwargs.pop('img_url', None)
        except KeyError:
            return
        
        image_filename = self.name.translate(str.maketrans('', '', PUNCTUATION)) + '.jpg'
            
        try:
            # image_url is a URL to the image which #marmiton is using
            result = urllib.request.urlretrieve(img_url) 
        except:
            return

        # self.photo is the ImageField
        self.image.save(
            os.path.join(image_filename),
            File(open(result[0], 'rb'))
            )

        super(Utensil, self).save(*args, **kwargs)
    
    def __str__(self):
        """ String Representation of the object of Utensil """
        return self.name

    class Meta:
        """ Meta Configurations of the class Utensil """
        # The order in which Utensils show on admin panel
        ordering = ['name']
        # The name which shows on the admin page
        verbose_name = _('Utensil')
        # The plural name which shows on the admin page
        verbose_name_plural = _('Utensils')


class IngredientItem(models.Model):
    """"
    It is and IngredientItem which is used for relating Ingredient and Recipe.
        There is One to Many relationship between IngredientItem and Ingredient
        There is One to Many relationship between Ingredient Item and Recipe
    - title: The name of the Ingredient i.e. Milk, Butter etc.
    - quantity: The quantity of the Ingredient 
    - ingredient: The Ingredient related to it
    - unit: The unit of the Ingredient i.e. Gram (g), Litre (l) etc.
    - recipe: The Recipe to which IngredientItem belongs to
    """
    quantity = models.CharField(max_length=10)
    ingredient = models.ForeignKey(to=Ingredient, 
                            on_delete=models.CASCADE)
    unit = models.CharField(max_length=10, #choices=UNITS,
                            help_text="Maximum 50 characters",
                            null=True, blank=True
                            )
    recipe = models.ForeignKey(to="Recipe", 
                            on_delete=models.CASCADE,
                            related_name='ingredients')

    def __str__(self):
        """ String representation of IngredientItem """
        return str(self.ingredient) + f"({self.quantity} {self.unit})"
    

class UtensilItem(models.Model):
    """
    It is a Utensil item which is used for relating Utensil with Recipe
        There is One to Many relationship between Utensil Item and Utensil
        There is One to Many relationship between Utensil Item and Recipe
    - title: The name of the Utensil i.e. Plates, Spoon etc.
    - quantity: The quantity of the Utensil
    - utensil: The Utensil related to it
    - recipe: The Recipe to which Utensil Item belongs to
    """
    quantity = models.CharField(max_length=10)
    utensil = models.ForeignKey(to=Utensil, 
                            on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", 
                            on_delete=models.CASCADE,
                            related_name='utensils')

    def __str__(self):
        """ String representation of UtensilItem """
        if self.quantity == '1':
            return f"{self.quantity} {self.utensil}" 
        # Add an s at the end of it is plural
        return f"{self.quantity} {self.utensil}s" 
        

class RecipeImage(models.Model):
    """"
    A Photo/Picture of a recipe
    There is a One to Many Relationship between Recipe and
    RecipeImage. Hence, there can be many images belonging 
    to a single Recipe.
    - image: The actual image or path to the image on server
    - recipe: The Recipe the image belongs to

    """
    image = models.ImageField(upload_to='recipe_images')
    recipe = models.ForeignKey("Recipe", related_name='recipe_images',
                                on_delete=models.CASCADE, null=True)

    def __str__(self):
        """ String Representation of the object of RecipeImage """
        return str(self.recipe) + " " + str(self.pk)
    
    
    class Meta:
        """ Meta Configurations of the class RecipeImage """
        verbose_name = _('Recipe Image')
        verbose_name_plural = _('Recipe Images')
        ordering = ['recipe']


class Recipe(models.Model):
    """"
    Recipe of a Food which consists of several fields and attributes
    Forexample:
    - title: Unique title of the Recipe i.e. Chinese Rice, Italian Pizza etc.
    - description: Free Text/Description or steps of making a recipe
    - slug: A unique url/slug of the Recipe i.e. chinese-rice-recipe etc.
    - preparation_time: The time it takes to make a recipe i.e. 10 min
    - cooking_time: The time it takes to cook the recipe
    - rest_time: The time it takes after cooking
    - difficulty: How much difficult it is to make the recipe i.e Easy, Medium
    - cost: The cost category which the Recipe belongs to i.e. Low, High 
    - approved: Whether the recipe is approved or not 
    - num_of_dishes: Initial number of dishes
    - video_url: Url/link to the Recipe video
    """
    title = models.CharField(unique=True, 
                            max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=120,
                                    null=False, blank=False)
    
    preparation_time = models.TimeField(default=time)
    cooking_time = models.TimeField(default=time)
    rest_time = models.TimeField(default=time)

    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    cost = models.CharField(max_length=1, choices=COST_CHOICES)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL,
                            blank=True, null=True, related_name='recipes')
    num_of_dishes = models.IntegerField()
    approved = models.BooleanField(null=False, default=False)
    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        """ String representation of the Recipe class"""
        return self.title

    @property
    def total_preparation_time(self):
        """ Calculates the sum of preparation time, cooking time and rest_time """

        preparation_timedelta = timedelta(hours=self.preparation_time.hour,
                                    minutes=self.preparation_time.minute)
        rest_timedelta = timedelta(hours=self.rest_time.hour, 
                                    minutes=self.rest_time.minute)
        cooking_timedelta = timedelta(hours=self.cooking_time.hour, 
                                    minutes=self.cooking_time.minute)

        total_timedelta = preparation_timedelta + rest_timedelta + cooking_timedelta
        
        hours = total_timedelta.seconds // 3600
        rest = total_timedelta.seconds % 3600
        minutes = rest // 60

        full_preparation_time = time(hour=hours, minute=minutes)

        return full_preparation_time

    @property
    def average_rating(self):
        """ Calculates average rating of all the review of the 
            current recipe and round it up to 1 decimal place. """
        ratings = self.reviews.values('rating') # Returns list of dictionaries
        # Loop through each dictionary of the list and get rating from it
        if ratings:
            average_rating = sum([int(rating.get('rating')) for rating in ratings])/len(ratings)
            average_rating = round(average_rating, 1)
            return average_rating
        return 0


    def save(self, *args, **kwargs):
        """ Overriding save method of models.Model to automatically 
        slugify each recipe using its title """
        ingredients = kwargs.pop('ingr', [])
        utensils = kwargs.pop('utns', [])
        recipe = kwargs.pop('rcp', None)
        
        try:
            self.slug = slugify(self.title)
            super(Recipe, self).save(*args, **kwargs)

            for ingredient in ingredients:
                IngredientItem(quantity=ingredient.quantity,
                                unit=ingredient.unit,
                                ingredient=Ingredient.objects.
                                filter(name=ingredient.name).first(),
                                recipe=self).save()

            for utensil in utensils:
                UtensilItem(quantity=utensil.quantity, 
                            utensil=Utensil.objects.
                            get(name=utensil.name),
                            recipe=self).save()

        
            if recipe:
                title = recipe.title
                image_filename = title.translate(str.maketrans('', '', PUNCTUATION)) + '.jpg'
                with open(f"media/recipe_images/{image_filename}", 'wb') as picture:
                    picture.write(recipe.recipe_image.image)

                #? Read the content of the file (Recipe Image) and create an
                #? instance of RecipImage
                recipeImageFile = File( open(f"media/recipe_images/{image_filename}", 'rb'))
                recipeImage = RecipeImage(image= recipeImageFile )
                recipeImage.recipe = self
                recipeImage.save()

                print(f"{recipeImage} saved")
                
            return True

        except IntegrityError:
            return False
           
    
    def get_quantity_of_ingredients_from_number_of_dishes(self, 
                                        current_num_of_dishes):
        """ A helper function which calculates the quantity for each
            ingredient of a recipe given current number of dishes.
        """
        quantities = []
        for ingredientItem in self.ingredients.all():
            quantity = ingredientItem.quantity
            if quantity:
                ratio = float(quantity) / self.num_of_dishes
                quantity = ratio * current_num_of_dishes

            quantities.append(quantity)
        return quantities

    
    @property
    def thumbnail_image(self):
        """ Returns url for thumbnail of the recipe from one of the
            many images it has. If no image then return the image
            of its category or default.jpg if there is no category 
            related to it.  """
        image = self.recipe_images.first()
        if image:
            return os.path.join(settings.STATIC_URL, image.image.url)
        if self.category:
            return os.path.join(settings.MEDIA_URL, self.category.image.url)
        return os.path.join(settings.STATIC_URL, 'img/default.jpg')

    @property
    def get_difficulty(self):
        for difficulty in DIFFICULTY_CHOICES:
            if difficulty[0] == self.difficulty:
                return difficulty[1]


    @property
    def get_cost(self):
        for cost in COST_CHOICES:
            if cost[0] == self.cost:
                return cost[1]
    class Meta:
        # ordering = ['title']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
