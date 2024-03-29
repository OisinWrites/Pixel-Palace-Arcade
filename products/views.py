from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Exists, OuterRef
from django.db.models.functions import Lower
from django.urls import reverse

from .models import Product, Category
from .forms import ProductForm
from review.forms import RatingForm
from review.models import Rating, Review
from profiles.models import Avatar


def all_products(request):
    """ A view to show all products and then handle sort and search queries"""
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                        description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search-term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show product details.
    This view has been enhanced to show info from the
    rating, review, and avatar profile models.
    """

    product = get_object_or_404(Product, pk=product_id)
    rating = None
    avatars = None
    reviews = None

    if request.user.is_authenticated:
        rating = Rating.objects.filter(
            product=product, user=request.user).first()
        reviews = Review.objects.filter(product=product).select_related('user')
        reviews = reviews.annotate(has_avatar=Exists(
            Avatar.objects.filter(user_id=OuterRef('user_id'))))
        user_ids = [review.user_id for review in reviews]
        avatars = Avatar.objects.filter(user_id__in=user_ids)
        avatar_dict = {avatar.user_id: avatar for avatar in avatars}
        for review in reviews:
            review.avatar = avatar_dict.get(review.user_id)

    if request.method == 'POST':
        if 'delete_rating' in request.POST:
            rating.delete()
            messages.info(request, 'Rating deleted successfully.')
            return redirect('product_detail', product_id=product_id)
        else:
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.user = request.user
                rating.product = product
                rating.save()
                messages.info(request, 'Rating added successfully.')
                return redirect('product_detail', product_id=product_id)
    else:
        form = RatingForm()

    context = {
        'form': form,
        'rating': rating,
        'product': product,
        'reviews': reviews if request.user.is_authenticated else [],
        'avatars': avatars if request.user.is_authenticated else [],
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
                Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit product"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. \
                Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


def search_view(request):
    query = request.GET.get('q')
    results = Product.search(query) if query else []
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'products/search.html', context)


@login_required
def product_management(request):
    if not request.user.is_superuser:
        messages.error(request, "Area Restricted. Returned to homepage.")
        return redirect('index')

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    # Handle search query
    query = None
    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('product_management'))

        # Use Q objects to filter by name or description containing the query
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

    # Existing code

    # Update context with the search-term
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/product_management.html', context)
