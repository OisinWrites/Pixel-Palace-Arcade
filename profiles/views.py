from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Avatar
from .forms import UserProfileForm, AvatarForm

from checkout.models import Order


@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    avatar = Avatar.objects.filter(user=profile.user).first()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        avatar_form.request = request

        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar = avatar_form.save(commit=False)
            avatar.user = request.user
            avatar.save()

            messages.success(request, 'Profile and avatar \
                updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Update failed. \
                Please ensure the forms are valid.')
    else:
        form = UserProfileForm(instance=profile)
        avatar_form = AvatarForm(instance=avatar)

    orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'avatar_form': avatar_form,
        'orders': orders,
        'on_profile_page': True,
        'avatar': avatar,
        'user_id': request.user.id,
    }
    return render(request, template, context)


def edit_avatar(request):
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


def order_history(request, order_number):
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
