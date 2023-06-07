from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
"""
This code is a function that calculates
the contents of the shopping bag.
It iterates over the items in the bag, calculates the total price,
quantity, and delivery cost based on the items and their prices.
It also determines if the total price qualifies for free delivery
based on the predefined threshold in settings.
The function returns a dictionary containing all
the calculated values for rendering in the templates.
"""


def bag_contents(request):
    # Initialize variables
    bag_items = []  # List to store items in the bag
    total = 0  # Total price of all items in the bag
    product_count = 0  # Total quantity of all products in the bag
    bag = request.session.get('bag', {})  # Retrieve bag data from the session

    # Iterate over items in the bag
    for item_id, item_data in bag.items():
        # Check if item_data is an integer (item without variants)
        if isinstance(item_data, int):
            # Retrieve the product using item_id
            product = get_object_or_404(Product, pk=item_id)
            # Calculate the price and quantity for the item
            total += item_data * product.price
            product_count += item_data
            # Append item details to bag_items list
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            # Retrieve the product using item_id
            product = get_object_or_404(Product, pk=item_id)
            # Iterate over variants and quantities in item_data
            for variant, quantity in item_data['items_by_variant'].items():
                # Calculate the price and quantity for the variant
                total += quantity * product.price
                product_count += quantity
                # Append variant item details to bag_items list
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variant': variant,
                })

    # Check if the total price is below the free delivery threshold
    if total < settings.FREE_DELIVERY_THRESHOLD:
        # Calculate the delivery cost as a percentage of the total price
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # Calculate the remaining amount for free delivery
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # No delivery cost if total price exceeds the free delivery threshold
        delivery = 0
        free_delivery_delta = 0

    # Calculate the grand total including delivery cost
    grand_total = delivery + total

    # Create a context dictionary with all the calculated values
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    # Return the context dictionary
    return context
