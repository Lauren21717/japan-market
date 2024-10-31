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
                messages.success(
                    request,
                    f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}',
                    extra_tags='update'
                )
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(
                    request,
                    f'Added size {size.upper()} {product.name} to your bag',
                    extra_tags='add'
                )
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(
                request,
                f'Added size {size.upper()} {product.name} to your bag',
                extra_tags='add'
            )
    else:
        if item_id in bag and isinstance(bag[item_id], dict):
            total_quantity = sum(bag[item_id]['items_by_size'].values())
            bag[item_id] = total_quantity + quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {bag[item_id]}',
                extra_tags='update'
            )
        else:
            bag[item_id] = bag.get(item_id, 0) + quantity
            messages.success(
                request,
                f'Added {product.name} to your bag',
                extra_tags='add'
            )

    request.session['bag'] = bag
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
                    messages.success(
                        request,
                        f'Updated size {size.upper()} {product.name} quantity to {quantity}',
                        extra_tags='update'
                    )
                else:
                    del bag[item_id]['items_by_size'][size]
                    if not bag[item_id]['items_by_size']:
                        bag.pop(item_id)
                    messages.success(
                        request,
                        f'Removed size {size.upper()} {product.name} from your bag',
                        extra_tags='remove'
                    )
            else:
                bag[item_id]['items_by_size'] = {size: quantity}
                messages.success(
                    request,
                    f'Updated size {size.upper()} {product.name} quantity to {quantity}',
                    extra_tags='update'
                )
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {quantity}',
                extra_tags='update'
            )
        else:
            bag.pop(item_id, None)
            messages.success(
                request,
                f'Removed {product.name} from your bag',
                extra_tags='remove'
            )

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the item from the shopping bag
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size', None)
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by-size']:
                bag.pop(item_id)
            messages.success(
                request,
                f'Removed size {size.upper()} {product.name} from your bag',
                extra_tags='remove'
            )
        else:
            bag.pop(item_id, None)
            messages.success(
                request,
                f'Removed {product.name} from your bag',
                extra_tags='remove'
            )

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request,
            f'Error removing item: {e}',
            extra_tags='error'
        )
        return HttpResponse(status=500)
