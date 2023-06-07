from django.shortcuts import render, redirect
from django.shortcuts import reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view to return the shopping bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the shopping bag
    """

    # Get the product object with the specified item_id from the database
    product = Product.objects.get(pk=item_id)

    # Extract the quantity of the product from the POST data of the request
    quantity = int(request.POST.get('quantity'))

    # Extract the redirect URL from the POST data of the request
    redirect_url = request.POST.get('redirect_url')

    # Initialize a variable to store the product variant (if any)
    variant = None

    # Check if the 'product_variant' key is present in the POST data
    if 'product_variant' in request.POST:
        variant = request.POST['product_variant']

    # Get the current bag from the session or
    # initialize an empty bag if it doesn't exist
    bag = request.session.get('bag', {})

    # Check if the product has a variant
    if variant:
        # Check if the item_id already exists in the bag
        if item_id in list(bag.keys()):
            # Check if the variant already exists for the item_id in the bag
            if variant in bag[item_id]['items_by_variant'].keys():
                # Update the quantity of the existing variant in the bag
                message_e = (f'Updated  {product.name} for {variant.upper()} '
                             f'quantity to '
                             f'{bag[item_id]["items_by_variant"][variant]}')
                bag[item_id]['items_by_variant'][variant] += quantity
                messages.success(request, message_e)
            else:
                # Add a new variant to the item_id in the bag
                message_a = (f'Added {product.name} for {variant.upper()} '
                             'to your bag')
                bag[item_id]['items_by_variant'][variant] = quantity
                messages.success(request, message_a)
        else:
            # Add a new item_id with a variant to the bag
            message_b = (f'Added {product.name} for {variant.upper()} '
                         'to your bag')
            bag[item_id] = {'items_by_variant': {variant: quantity}}
            messages.success(request, message_b)
    else:
        # The product does not have a variant
        # Check if the item_id already exists in the bag
        if item_id in list(bag.keys()):
            # Update the quantity of the existing item_id in the bag
            message_c = f'Updated {product.name} quantity to {bag[item_id]}'
            bag[item_id] += quantity
            messages.success(request, message_c)
        else:
            # Add a new item_id without a variant to the bag
            message_d = f'Added {product.name} to your bag'
            bag[item_id] = quantity
            messages.success(request, message_d)

    # Update the bag in the session with the modified or new items
    request.session['bag'] = bag

    # Redirect to the specified URL
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Add or remove a quantity of the specified product
    to the shopping bag """

    # Get the product object with the specified item_id from the database or
    # return a 404 error if not found
    product = get_object_or_404(Product, pk=item_id)

    # Extract the quantity of the product from the POST data of the request
    quantity = int(request.POST.get('quantity'))

    # Initialize a variable to store the product variant (if any)
    variant = None

    # Check if the 'product_variant' key is present in the POST data
    if 'product_variant' in request.POST:
        variant = request.POST['product_variant']

    # Get the current bag from the session or initialize
    # an empty bag if it doesn't exist
    bag = request.session.get('bag', {})

    # Check if the product has a variant
    if variant:
        # Check if the quantity is greater than 0
        if quantity > 0:
            # Update the quantity of the variant in the bag
            bag[item_id]['items_by_variant'][variant] = quantity
            messages.success(
                request, f'Updated {product.name} for {variant.upper()} '
                f'quantity to {bag[item_id]["items_by_variant"][variant]}'
                )
        else:
            # Remove the variant from the item_id in the bag
            del bag[item_id]['items_by_variant'][variant]
            if not bag[item_id]['items_by_variant']:
                # If there are no more variants for the item_id,
                # remove the item_id from the bag
                bag.pop(item_id)
            messages.success(request, f'Removed {product.name} for '
                             f'{variant.upper()} from your bag')
    else:
        # The product does not have a variant
        # Check if the quantity is greater than 0
        if quantity > 0:
            # Update the quantity of the item_id in the bag
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} '
                             f'quantity to {bag[item_id]}')
        else:
            # Remove the item_id from the bag
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    # Update the bag in the session with the modified or removed items
    request.session['bag'] = bag

    # Redirect to the 'view_bag' page
    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """ Remove the specified product, or variant thereof,
    from the shopping bag """

    try:
        # Get the product object with the specified item_id
        # from the database or return a 404 error if not found
        product = get_object_or_404(Product, pk=item_id)

        # Initialize a variable to store the product variant (if any)
        variant = None

        # Check if the 'product_variant' key is present in the POST data
        if 'product_variant' in request.POST:
            variant = request.POST['product_variant']

        # Get the current bag from the session or initialize an
        # empty bag if it doesn't exist
        bag = request.session.get('bag', {})

        # Check if the product has a variant
        if variant:
            # Remove the variant from the item_id in the bag
            del bag[item_id]['items_by_variant'][variant]

            # If there are no more variants for the item_id, remove
            # the item_id from the bag
            if not bag[item_id]['items_by_variant']:
                bag.pop(item_id)

            message_a = (
                f'Removed variant {variant.upper()}'
                f'{product.name} from your bag'
                )
            messages.success(request, message_a)
        else:
            # Remove the item_id from the bag
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        # Update the bag in the session with the removed item or variant
        request.session['bag'] = bag

        # Return an HTTP response with a success status code (200)
        return HttpResponse(status=200)
    except Exception as e:
        # If an exception occurs, display an error message
        # return an HTTP response with an error status code (500)
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
