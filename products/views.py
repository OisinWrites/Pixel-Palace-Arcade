from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def all_products(request):
    """ A view to show all products and then handle sort and search queries"""
    products = Product.objects.all()
    # filter top-level categories

    context = {
        'products': products,
        }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show product details"""
    product = get_object_or_404(Product, pk=product_id)
    # filter top-level categories

    context = {
        'product': product,
        }

    return render(request, 'products/product_detail.html', context)
