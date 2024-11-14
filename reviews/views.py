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


@login_required
def edit_review(request,product_id, product_review_id):
    """
    A view to return the edit product review page
    """
    review = get_object_or_404(ProductReview, pk=product_review_id)
    product = get_object_or_404(Product, id=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the review author
    if request.user != review.user_profile.user:
        messages.error(
            request,
            'Forbidden: You are not allowed to edit review.'
        )
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(
                request,
                'Failed to update review. Please ensure the form is valid.'
            )
    else:
        form = ProductReviewForm(instance=review)

    context = {
        'form': form,
        'product': product,
        'review': review,
    }
    return render(request, 'reviews/edit_review.html', context)


@login_required
def delete_review(request, product_review_id):
    """
    Delete a product review
    """
    review = get_object_or_404(ProductReview, pk=product_review_id)

    # Check if the user is the author of the review or an admin
    if request.user != review.user_profile.user and not request.user.is_superuser:
        messages.error(
            request,
            'You are not authorized to delete this review.'
        )
        return redirect('product_detail', product_id=review.product.id)

    # Delete the review and show a success message
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('product_detail', product_id=review.product.id)