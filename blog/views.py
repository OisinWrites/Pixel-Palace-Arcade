from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from django import forms
from .forms import ReviewForm
from products.models import Product


def create_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('blog/create_review.html', pk=product_id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
    }

    return render(request, 'blog/create_review.html', context)


def view_reviews(request, product_id):
    """ A view to show reviews"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        }

    return render(request, 'blog/review.html', context)


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
    review = get_object_or_404(Review, id=review_id)
    product_id = review.product.id
    review.delete()
    return redirect('product_detail', id=product_id)
