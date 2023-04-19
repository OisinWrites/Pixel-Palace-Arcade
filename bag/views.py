from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    """ A view to return the shopping bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    variant = None
    if 'product_variant' in request.POST:
        variant = request.POST['product_variant']
    bag = request.session.get('bag', {})

    if variant:
        if item_id in list(bag.keys()):
            if variant in bag[item_id]['items_by_variant'].keys():
                message_e = (f'Updated  {product.name} for {variant.upper()} '
                             f'quantity to'
                             f'{bag[item_id]["items_by_variant"][variant]}')
                bag[item_id]['items_by_variant'][variant] += quantity
                messages.success(request, message_e)
            else:
                message_a = (f'Added {product.name} for {variant.upper()} '
                             'to your bag')
                bag[item_id]['items_by_variant'][variant] = quantity
                messages.success(request, message_a)
        else:
            message_b = (f'Added {product.name} for {variant.upper()} '
                         'to your bag')
            bag[item_id] = {'items_by_variant': {variant: quantity}}
            messages.success(request, message_b)
    else:
        if item_id in list(bag.keys()):
            message_c = f'Updated {product.name} quantity to {bag[item_id]}'
            bag[item_id] += quantity
            messages.success(request, message_c)
        else:
            message_d = f'Added {product.name} to your bag'
            bag[item_id] = quantity
            messages.success(request, message_d)

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Add or remove a quantity of the specified product
    to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    variant = None
    if 'product_variant' in request.POST:
        variant = request.POST['product_variant']
    bag = request.session.get('bag', {})

    if variant:
        if quantity > 0:
            bag[item_id]['items_by_variant'][variant] = quantity
            messages.success(request, f'Updated {product.name} for '
                             f'{variant.upper()} quantity to'
                             f'{bag[item_id]["items_by_variant"][variant]}')
        else:
            del bag[item_id]['items_by_variant'][variant]
            if not bag[item_id]['items_by_variant']:
                bag.pop[item_id]
            messages.success(request, f'Removed {product.name} for '
                                      f'{variant.upper()} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} '
                             f'quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """ Remove the specified product, or variant thereof,
    from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        variant = None
        if 'product_variant' in request.POST:
            variant = request.POST['product_variant']
        bag = request.session.get('bag', {})

        if variant:
            del bag[item_id]['items_by_variant'][variant]
            if not bag[item_id]['items_by_variant']:
                bag.pop(item_id)
            message_a = (f'Removed variant {variant.upper()} '
                         f'{product.name} from your bag')
            messages.success(request, message_a)
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
