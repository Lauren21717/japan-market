from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, UserNameUpdateForm, CustomerPasswordChangeForm
from checkout.models import Order


@login_required
def profile(request):
    """
    Display the user's profile.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'profiles/profile.html'
    context={
        'user': request.user,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def account_detail(request):
    """
    Display and update the user's account details.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Delivery Information Form
        if 'profile_submit' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Delivery information updated successfully')
            else:
                messages.error(request, 'Update failed. Please ensure the form is valid.')

        # Update Username Form
        elif 'username_submit' in request.POST:
            username_form = UserNameUpdateForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Username updated successfully')
            else:
                messages.error(request, 'Username update failed. Please ensure the username is valid.')

        # Update Password Form 
        elif 'password_submit' in request.POST:
            password_form = CustomerPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Password update failed. Please correct the errors below.')

    profile_form = UserProfileForm(instance=profile)
    username_form = UserNameUpdateForm(instance=request.user)
    password_form = CustomerPasswordChangeForm(request.user)

    template = 'profiles/account_detail.html'
    context = {
        'profile_form': profile_form,
        'username_form': username_form,
        'password_form': password_form,
        'user': request.user,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def order_history_list(request):
    """
    Display list of all orders for the user.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all().order_by('-date')

    template = 'profiles/order_history.html'
    context = {
        'orders': orders,
        'user': request.user,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def order_detail(request, order_number):
    """
    Display individual order details.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
