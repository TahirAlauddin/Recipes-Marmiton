from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import *



class UtensilAdmin(admin.ModelAdmin):
    model = Utensil
    list_display = ('name',)
    search_fields = ('name',)
    

class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'approved')
    search_fields = ('name',)
    actions = ['approve_ingredients']

    
    @admin.action(description='Approve Ingredients')
    def approve_ingredients(self, request, queryset):
        for ingredient in queryset:
            ingredient.approved = True
            ingredient.save()
        count = len(queryset)
        self.message_user(request, ngettext(
            '%d ingredient was approved successfully.',
            '%d ingredients were approved successfully.',
            count ) % count, messages.SUCCESS)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'approved', 'cost', 'difficulty', 'prep_time',)
    list_filter = ('category', 'cost', 'difficulty',)
    search_fields = ('title', 'category__name',)
    prepopulated_fields = {'slug': ('title',)}
    model = Recipe
    actions = ['approve_recipes']

    @admin.action(description='Approve Recipes')
    def approve_recipes(self, request, queryset):
        for recipe in queryset:
            recipe.approved = True
            recipe.save()
        count = len(queryset)
        self.message_user(request, ngettext(
            '%d recipe was approved successfully.',
            '%d recipes were approved successfully.',
            count ) % count, messages.SUCCESS)

    @admin.display(empty_value='???')
    def prep_time(self, obj):
        time = f"{obj.preparation_time.minute} minutes"
        if obj.preparation_time.hour:
            time = f"{obj.preparation_time.hour} hours" + time
        return time



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Utensil, UtensilAdmin)
admin.site.register(RecipeImage)
admin.site.register(IngredientItem)
admin.site.register(UtensilItem)
