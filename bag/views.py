from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view to return the shopping bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    variant = None
    if 'product_variant' in request.POST:
        variant = request.POST['product_variant']
    bag = request.session.get('bag', {})

    if variant:
        if item_id in list(bag.keys()):
            if variant in bag[item_id]['items_by_variant'].keys():
                bag[item_id]['items_by_variant'][variant] += quantity
            else:
                bag[item_id]['items_by_variant'][variant] = quantity
        else:
            bag[item_id] = {'items_by_variant': {variant: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
