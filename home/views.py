from django.shortcuts import render
from collection.models import Product, Category
from django.db.models import Q

# Create your views here.


def index(request):
    """
    A view to return the home page
    """
    categories = Category.objects.exclude(name='all_collections')

    products = Product.objects.filter(
        Q(is_special_offer=True) | Q(is_featured=True)
    )[:4]

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'home/index.html', context)
