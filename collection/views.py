from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, ShopByOption


def collection(request):
    """
    A view to show all products, including sorting and search queries
    """
    products = Product.objects.all()
    query = None
    categories = None
    shop_by_options = None

    if request.GET:
        # Search Query
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('collection'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        
        # Category Filtering
        if 'category' in request.GET:
            category_names = request.GET['category'].split(',')
            products = products.filter(category__name__in=category_names)
            categories = Category.objects.filter(name__in=category_names)

        # Shop By Options Filtering
        if 'shop_by_option' in request.GET:
            shop_by_option_names = request.GET['shop_by_option'].split(',')
            products = products.filter(shop_by__name__in=shop_by_option_names)
            shop_by_options = ShopByOption.objects.filter(name__in=shop_by_option_names)

        # Clearance (Special Offer) Filtering
        if 'offer' in request.GET:
            products = products.filter(is_special_offer=True)

        # New Arrivals (Featured Products) Filtering
        if 'new_arrivals' in request.GET:
            products = products.filter(is_featured=True)

        # All Specials (Both Special Offer and Featured Products)
        if 'all_specials' in request.GET:
            products = products.filter(Q(is_special_offer=True) | Q(is_featured=True))
    
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_shop_by_options': shop_by_options,
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
