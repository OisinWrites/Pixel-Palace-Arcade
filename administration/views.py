from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from .forms import NewsletterSubscriptionForm

import json
from django.http import JsonResponse, HttpResponseRedirect

from .forms import MarkOrderCompletedForm, MarkOrderIncompleteForm
from .forms import MonthYearFilterForm
from checkout.models import Order

from profiles.models import Avatar, UserProfile
from .models import Subscriber


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
                    print(f"Order {order_id} marked as completed.")
                except Order.DoesNotExist:
                    pass

        except json.JSONDecodeError:
            pass

        # Process individual order form submission
        order_id = request.POST.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.completed = True
                order.save()
                """_send_shipping_confirmation_email(order)"""
                print(f"Order {order_id} marked as completed.")

            except Order.DoesNotExist:
                pass

        return redirect('pending_orders')


def completed_orders(request):
    complete_orders = Order.objects.filter(completed=True)

    if request.method == 'POST':
        # Handle the cancel form submission
        cancel_form = MarkOrderIncompleteForm(request.POST)
        if cancel_form.is_valid():
            order_id = cancel_form.cleaned_data.get('order_id')
            try:
                order_to_cancel = Order.objects.get(id=order_id)
                order_to_cancel.completed = False
                order_to_cancel.save()
                # Redirect to the same page after canceling the order
                return redirect('completed_orders')
            except Order.DoesNotExist:
                # Handle the case where the order doesn't exist
                pass

    # Handle the filter form submission
    filter_form = MonthYearFilterForm(request.GET)
    if filter_form.is_valid():
        month = filter_form.cleaned_data.get('month')
        year = filter_form.cleaned_data.get('year')
        hour = filter_form.cleaned_data.get('hour')
        day = filter_form.cleaned_data.get('day')

        if month:
            complete_orders = complete_orders.filter(date__month=month)
        if year:
            complete_orders = complete_orders.filter(date__year=year)
        if hour:
            complete_orders = complete_orders.filter(date__hour=hour)
        if day:
            complete_orders = complete_orders.filter(date__day=day)

    # Handle the search query
    search_query = request.GET.get('search')
    if search_query:
        complete_orders = complete_orders.filter(
            Q(full_name__icontains=search_query) | Q(
                order_number__icontains=search_query)
        )

    cancel_form = MarkOrderIncompleteForm()
    context = {
        'cancel_form': cancel_form,
        'filter_form': filter_form,
        'complete_orders': complete_orders,
    }

    return render(request, 'administration/completed_orders.html', context)


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


@login_required
def newsletter_signup(request):
    # Make sure the user is authenticated before proceeding
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL

    user = request.user

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congrats! Thank you for signing up, \
                    you'll love our amazing deals!")
            return redirect('home')
    else:
        form = NewsletterSubscriptionForm(user=user)

    context = {
        'form': form
    }
    return render(request, 'administration/newsletter_signup.html', context)


def newsletter_list(request):
    # Retrieve all user profiles where newsletter_subscribed is True
    subscribers = Subscriber.objects.filter(
        newsletter_subscribed=True)

    context = {
        'subscribers': subscribers
    }
    return render(request, 'administration/newsletter_list.html', context)


def newsletter_unsubscribe(request, subscriber_id):
    subscriber = get_object_or_404(UserProfile, id=subscriber_id)

    if request.user != subscriber.user:
        # Redirect the user to the homepage if they are
        # not the subscription owner
        messages.error(request, "Sorry, you can't cancel \
            someone else's subscription.")
        return redirect('home')

    if request.method == 'POST':
        # Toggle the newsletter_subscribed field to False and save the changes
        subscriber.newsletter_subscribed = False
        subscriber.save()
        return redirect('home')

    context = {
        'subscriber': subscriber
    }
    return render(
        request, 'administration/newsletter_unsubscribe.html', context)


def toggle_subscription(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, id=subscriber_id)

    if request.user != subscriber.user:
        messages.error(request,
                       "Sorry, you can't cancel someone else's subscription.")
        return redirect('home')

    if request.method == 'POST':
        # Toggle the newsletter_subscribed field
        subscriber.newsletter_subscribed = not subscriber.newsletter_subscribed
        subscriber.save()
        return redirect('profile')

    return redirect('profile')
