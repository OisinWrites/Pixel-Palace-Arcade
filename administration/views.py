from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

import json
from django.http import JsonResponse

from .forms import MarkOrderCompletedForm, MarkOrderIncompleteForm
from checkout.models import Order

from profiles.models import Avatar, UserProfile


def pending_orders(request):

    if request.method == 'GET':
        incomplete_orders = Order.objects.filter(completed=False)

        form = MarkOrderCompletedForm()
        context = {
            'incomplete_orders': incomplete_orders,
            'form': form
        }

        return render(request, 'administration/pending_orders.html', context)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_ids = data.get('order_ids', [])

            for order_id in order_ids:
                try:
                    order = Order.objects.get(id=order_id)
                    order.completed = True
                    order.save()

                    """_send_shipping_confirmation_email(order)"""

                except Order.DoesNotExist:
                    pass

        except json.JSONDecodeError:
            pass

    return redirect('pending_orders')


def completed_orders(request):

    if request.method == 'GET':
        complete_orders = Order.objects.filter(completed=True)

        form = MarkOrderIncompleteForm()
        context = {
            'complete_orders': complete_orders,
        }

        return render(request, 'administration/completed_orders.html', context)

    elif request.method == 'POST':
        form = MarkOrderIncompleteForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            order = Order.objects.get(id=order_id)
            order.completed = False
            order.save()

            order = Order.objects.get(id=order_id)
            print(order.email)

            """_send_shipping_confirmation_email(order)"""

            messages.success(request, f'Shipment canceled. \
                    A notification email will be sent to {order.email}.')

            return redirect('completed_orders')


def _send_shipping_confirmation_email(order):
    """Send the user a shipping confirmation email"""
    cust_email = order.email
    subject = render_to_string(
        'checkout/confirmation_emails/shipping_email_subject.txt',
        {'order': order}
    )
    body = render_to_string(
        'checkout/confirmation_emails/shipping_email_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
    )

    # Print the email content to the terminal
    print("Subject: ", subject)
    print("Body: ", body)

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )


@login_required
def admin_menu(request):
    if not request.user.is_superuser:
        messages.error(request, "Area Restricted. Returned to homepage.")
        return redirect('index')

    profile = get_object_or_404(UserProfile, user=request.user)
    avatar = Avatar.objects.filter(user=profile.user).first()

    context = {
        'avatar': avatar,
    }

    return render(request, 'administration/admin_menu.html', context)
