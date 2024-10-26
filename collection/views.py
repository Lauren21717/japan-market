from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404

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


def product_detail(request, product_id):
    """
    A view to show individual product details
    """
    
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'collection/product_detail.html', context)