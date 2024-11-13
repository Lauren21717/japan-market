from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ProductReview
from .forms import ProductReviewForm
from collection.models import Product
from profiles.models import UserProfile


@login_required
def add_review(request, product_id):
    """
    A view to return the add product review page
    """
    product = get_object_or_404(Product, id=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user has purchased the product
    if not profile.user_purchases.filter(id=product.id).exists():
        messages.error(
            request,
            'Sorry, you need to purchase this product before adding a review.'
        )
        return redirect('product_detail', product_id=product.id)

    # Check if the user has already reviewed the product
    already_review = ProductReview.objects.filter(
        product=product, user_profile=profile
    ).exists()
    if already_review:
        messages.error(request, "You have already reviewed this product.")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user_profile = profile
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Failed to add review, please ensure the form is valid.')
    else:
        form = ProductReviewForm()

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'reviews/add_review.html', context)

