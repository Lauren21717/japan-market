from django.shortcuts import (
    render, redirect, HttpResponse, reverse, get_object_or_404
    )
from django.contrib import messages
from collection.models import Product

def view_bag(request):
    """
    A view that renders the bag contents page
    """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size', None)
    bag = request.session.get('bag', {})

    if size:
        if item_id in bag and isinstance(bag[item_id], int):
            bag[item_id] = {'items_by_size': {}}
        
        if item_id in bag:
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in bag and isinstance(bag[item_id], dict):
            total_quantity = sum(bag[item_id]['items_by_size'].values())
            bag[item_id] = total_quantity + quantity
        else:
            bag[item_id] = bag.get(item_id, 0) + quantity

    request.session['bag'] = bag
    messages.success(request, f'Added {product.name} to your bag')
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size', None)
    bag = request.session.get('bag', {})

    if size:
        if item_id in bag:
            if 'items_by_size' in bag[item_id]:
                if quantity > 0:
                    bag[item_id]['items_by_size'][size] = quantity
                else:
                    del bag[item_id]['items_by_size'][size]
                    if not bag[item_id]['items_by_size']:
                        bag.pop(item_id)
            else:
                bag[item_id]['items_by_size'] = {size: quantity}
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id, None)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))



