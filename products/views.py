from django.shortcuts import render
from .models import Category, Product


def all_products(request):
    """ A view to show all products and then handle sort and search queries"""
    products = Product.objects.all()
    # filter top-level categories

    context = {
        'products': products,
        }

    return render(request, 'products/products.html', context)


def filter_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    subcategories = category.category_set.all()
    # get subcategories

    context = {
        'products': products,
        'categories': subcategories,
        'selected_category': category
        }

    return render(request, 'product_list.html', context)
