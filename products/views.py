from django.shortcuts import render
from .models import Category, Product


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.filter(parent_category__isnull=True)
    # filter top-level categories
    return render(request, 'product_list.html', {'products': products,
                                                 'categories': categories})


def filter_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    subcategories = category.category_set.all()
    # get subcategories
    return render(request, 'product_list.html', {'products': products,
                  'categories': subcategories, 'selected_category': category})
