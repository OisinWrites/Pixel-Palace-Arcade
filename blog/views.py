from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from django import forms
from django.contrib import messages
from .forms import ReviewForm
from products.models import Product
from .models import Rating
from django.urls import reverse


def create_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    rating = Rating.objects.filter(product=product, user=request.user).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.info(request, 'New review added')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'rating': rating,
        'product': product,
    }

    return render(request, 'blog/create_review.html', context)


def view_reviews(request, product_id):
    """ A view to show reviews"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        }

    return render(request, 'blog/reviews.html', context)


def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/update_review.html', {'form': form})


def delete_review(request, review_id):
    """Delete a review"""
    if not request.user.is_authenticated:
        messages.error(request, "Sorry, \
            you can't access other user's profiles.")
        return redirect('product_detail', id=product_id)

    review = get_object_or_404(Review, id=review_id)
    product_id = review.product.id 
    review.delete()
    messages.info(request, 'Review deleted!')
    return redirect(
        reverse('product_detail', kwargs={'product_id': product_id}))
