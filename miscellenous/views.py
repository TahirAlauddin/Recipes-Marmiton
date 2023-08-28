from django.shortcuts import render
from .models import Category


# View for category page
def view_category(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'recipes/category.html', context=context)


# View for category detail page
def view_category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    context = {'category': category}
    return render(request, 'recipes/category_detail.html', context=context)

