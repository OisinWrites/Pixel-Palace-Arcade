from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Avatar
from .forms import UserProfileForm, AvatarForm
from review.models import Review, Rating
from products.models import Product

from checkout.models import Order


@login_required
def profile(request):
    """
    Profile view shows the users avatar, saved default data,
    completed orders and review history.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    avatar = Avatar.objects.filter(user=profile.user).first()

    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        avatar_form.request = request

        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar = avatar_form.save(commit=False)
            avatar.user = request.user
            avatar.save()

            messages.success(
                request, 'Profile and avatar updated successfully')
            return redirect('profile')
        else:
            # Display form errors for debugging
            for field, error in form.errors.items():
                messages.error(request, f"Form Error ({field}): {error}")
            for field, error in avatar_form.errors.items():
                messages.error(
                    request, f"Avatar Form Error ({field}): {error}")
    else:
        form = UserProfileForm(instance=profile)
        avatar_form = AvatarForm(instance=avatar)

    orders = profile.orders.all()
    reviews = Review.objects.filter(user=request.user)

    ratings = {}
    for review in reviews:
        product = review.product
        rating = Rating.objects.filter(
            product=product, user=request.user).first()
        ratings[product.id] = rating

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'avatar_form': avatar_form,
        'orders': orders,
        'reviews': reviews,
        'on_profile_page': True,
        'avatar': avatar,
        'user_id': request.user.id,
        'ratings': ratings,
    }
    return render(request, template, context)


@login_required
def update_delivery_info(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Delivery information updated successfully')
        else:
            # Display form errors for debugging
            for field, error in form.errors.items():
                messages.error(request, f"Form Error ({field}): {error}")

    return redirect('profile')


def edit_avatar(request):
    """
    This view allows users to edit their existing avatar
    similarly to how existing products are edited.
    """
    avatar = get_object_or_404(Avatar, user=request.user)

    if request.method == 'POST':
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        avatar_form.request = request

        if avatar_form.is_valid():
            avatar = avatar_form.save(commit=False)
            avatar.user = request.user
            avatar.save()

            messages.success(request, 'Avatar updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Update failed. \
                Please ensure the form is valid.')
    else:
        avatar_form = AvatarForm(instance=avatar)

    template = 'profiles/edit_avatar.html'
    context = {
        'avatar_form': avatar_form,
        'avatar': avatar,
    }
    return render(request, template, context)


def delete_avatar(request):
    """Delete a user's avatar"""
    avatar = get_object_or_404(Avatar, user=request.user)
    avatar.delete()
    messages.success(request, 'Avatar deleted successfully')
    return redirect('profile')


def order_history(request, order_number):
    """
    This view stores the info from successful purchases for each user.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order nubmer { order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
