from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import MarkOrderCompletedForm
from checkout.models import Order

from profiles.models import Avatar, UserProfile


def admin_order_list(request):

    if request.method == 'GET':
        incomplete_orders = Order.objects.filter(completed=False)

        form = MarkOrderCompletedForm()
        context = {
            'incomplete_orders': incomplete_orders,
            'form': form
        }

        return render(request, 'administration/admin_order_list.html', context)

    elif request.method == 'POST':
        form = MarkOrderCompletedForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            order = Order.objects.get(id=order_id)
            order.completed = True
            order.save()

            order = Order.objects.get(id=order_id)
            print(order.email)

            """_send_shipping_confirmation_email(order)"""

            messages.success(request, f'Order Shipped! \
                    A shipping confirmation \
                    email will be sent to {order.email}.')

            return redirect('admin_order_list')

    return redirect('admin_order_list')


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


def admin_menu(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    avatar = Avatar.objects.filter(user=profile.user).first()

    context = {
        'avatar': avatar,
    }

    return render(request, 'administration/admin_menu.html', context)
