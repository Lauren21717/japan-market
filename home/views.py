from django.shortcuts import render
from collection.models import Product, Category

# Create your views here.

def index(request):
    """
    A view to return the home page
    """
    categories = Category.objects.exclude(name='all_collections')
    context = {
        'categories': categories,
    }
    return render(request, 'home/index.html', context)