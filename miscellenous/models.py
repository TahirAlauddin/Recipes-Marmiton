from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.text import slugify


DEFAULT_CHOICES = (
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
)

class Category(models.Model):
    """"
    The Category of a product, in this case the Recipe.
    name
    - name: A unique name/title of a Category
    - slug: A unique Slug/Url of a Category
    """
    name = models.CharField(max_length=120,
                            unique=True,
                            help_text="Maximum 120 characters",
                            )
    slug = models.SlugField(unique=True, 
                            help_text='Automatically generated from the title')
    image = models.ImageField(default='default_category.jpg', upload_to='categories')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Overriding save method of models.Model to automatically 
        slugify each recipe using its name """

        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    

class Review(models.Model):
    """
    Represents a user review, which includes free text
    - reviewed_recipe: Recipe, which is reviewed.
    - user: User, which posted the rating.
    - content (optional): Running text.
    - creation_date: The date and time, this review was created.
    - rating: The Rating, which a user has given to the review.
        i.e. 5, 4, 3, 2, 1
    """
    recipe = models.ForeignKey(to="recipes.Recipe", on_delete=models.CASCADE,
                                related_name='reviews', null=True)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True)
    rating = models.CharField(max_length=1, choices=DEFAULT_CHOICES,
                                blank=False, null=False)
    content = models.TextField( max_length=1024,
                                blank=True,null=True,
                                )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    def get_owner(self):
        """Returns the owner who wrote this review or ``Anonymous``."""
        if self.owner:
            return self.owner.username
        return _('Anonymous')

    def is_editable(self):
        """
        Returns True, if the time period to update this review hasn't ended
        yet.
        If the period setting has not been set, it always return True. This
        is the general case. If the user has used this setting to define an
        update period it returns False, if this period has expired.

        Set REVIEW_UPDATE_PERIOD in settings.py to number of hours you want to 
        make a review editable
        """
        if getattr(settings, 'REVIEW_UPDATE_PERIOD', False):
            period_end = self.creation_date + timezone.timedelta(
                seconds=getattr(settings, 'REVIEW_UPDATE_PERIOD') * 3600)
            if timezone.now() > period_end:
                return False
        return True

    def __str__(self):
        return f'{self.recipe} - {self.get_owner()}'
        
    class Meta:
        ordering = ['-creation_date']
