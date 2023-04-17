from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from django import Forms
from .forms import ReviewForm

def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form})

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