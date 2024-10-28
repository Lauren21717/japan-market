from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, ShopByOption


def collection(request):
    """
    A view to show all products, including sorting and search queries
    """
    products = Product.objects.all()
    query = None
    categories = None
    shop_by_options = None
    sort = None
    direction = None
    page_header = "All Collections"
    page_description = "Browse our full range of products across various categories, from essentials to exclusive items, crafted to meet your every need."

    if request.GET:
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            # Handling sorting by different fields
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            elif sortkey == 'category':
                sortkey = 'category__name'
            elif sortkey == 'shop_by_option':
                sortkey = 'shop_by__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
  
            products = products.order_by(sortkey)

        # Category Filtering
        if 'category' in request.GET:
            category_names = request.GET['category'].split(',')
            products = products.filter(category__name__in=category_names)
            categories = Category.objects.filter(name__in=category_names)
            if len(category_names) == 1:
                category = Category.objects.get(name=category_names[0])
                page_header = category.header
                page_description = category.description

        # Shop By Options Filtering
        if 'shop_by_option' in request.GET:
            shop_by_option_names = request.GET['shop_by_option'].split(',')
            products = products.filter(shop_by__name__in=shop_by_option_names)
            shop_by_options = ShopByOption.objects.filter(name__in=shop_by_option_names)
            if len(shop_by_option_names) == 1:
                shop_by_option = ShopByOption.objects.get(name=shop_by_option_names[0])
                category = shop_by_option.category
                page_header = f"{shop_by_option.friendly_name}"
                page_description = category.description

        # Clearance (Special Offer) Filtering
        if 'offer' in request.GET:
            page_header = "Special Offers"
            page_description = "Grab limited-time discounts on selected items."
            products = products.filter(is_special_offer=True)

        # New Arrivals (Featured Products) Filtering
        if 'new_arrivals' in request.GET:
            page_header = "New Arrivals"
            page_description = "Discover our latest additions to the collection."
            products = products.filter(is_featured=True)

        # All Specials (Both Special Offer and Featured Products)
        if 'all_specials' in request.GET:
            products = products.filter(Q(is_special_offer=True) | Q(is_featured=True))
            page_header = "Exclusive Specials"
            page_description = "Discover exclusive deals and the latest additions in one place. Shop now for limited-time discounts and fresh new products!"

        # Search Query
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('collection'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_shop_by_options': shop_by_options,
        'current_sorting': current_sorting,
        'page_header': page_header,
        'page_description': page_description,
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
