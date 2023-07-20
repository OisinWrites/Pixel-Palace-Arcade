from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from django import forms
from django.contrib import messages
from .forms import ReviewForm
from products.models import Product
from .models import Rating
from django.urls import reverse


def create_review(request, product_id):
    """
    View function for creating a new review for a product,
    and passes in the rating model to show in the template also.
    """

    product = get_object_or_404(Product, pk=product_id)
    existing_review = Review.objects.filter(
        product=product, user=request.user).first()

    if existing_review:
        # If the user has already submitted a review,
        # redirect to the update_review URL
        return redirect('update_review', review_id=existing_review.id)

    rating = Rating.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST':
        # If the request method is POST, process the submitted form data
        form = ReviewForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the review to the database
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.info(request, 'New review added')
            return redirect('product_detail', product_id=product_id)
    else:
        # If the request method is GET, display an empty form
        form = ReviewForm()

    context = {
        'form': form,
        'rating': rating,
        'product': product,
    }

    return render(request, 'review/create_review.html', context)


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Check if the current user is the owner of the review
    if request.user != review.user:
        # Redirect the user to the homepage if they are not the review's owner
        return redirect('home')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            if review.product:
                return redirect('product_detail', product_id=review.product.id)
            else:
                return redirect('home')
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'product': review.product,
    }

    return render(request, 'review/update_review.html', context)


def delete_review(request, review_id):
    """Delete a review"""

    # Handles interference from a malicious actor
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


def review_modal(request, review_id):
    # Fetch the review based on the review_id
    review = get_object_or_404(Review, id=review_id)

    context = {
        'review': review,
    }
    return render(
        request, 'review/includes/review-content-modal.html', context
        )
