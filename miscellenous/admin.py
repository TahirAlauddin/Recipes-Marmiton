from django.contrib import admin
from .models import Review, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


admin.site.register(Review)
admin.site.register(Category, CategoryAdmin)
