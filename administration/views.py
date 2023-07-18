from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import MarkOrderCompletedForm
from checkout.models import Order


def admin_order_list(request):

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

            _send_shipping_confirmation_email(order)

            messages.success(request, f'Order Shipped! \
                    A shipping confirmation \
                    email will be sent to {order.email}.')

            return redirect('admin_order_list')

    return redirect('admin_order_list')
