from django.shortcuts import render
from .models import Product

# Create your views here.

def collection(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Product.objects.all()
    
    context = {
        'products': products,
    }
    
    return render(request, 'collection/collection.html', context)