from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.conf import settings

from .models import Order


class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_checkout_view_get(self):
        # Create a session with some bag items
        self.client.post(
            reverse('add_to_bag', args=[product_id]), {'quantity': 1}
            )
        session = self.client.session
        session['bag'] = {'1': 1}
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIn('stripe_public_key', response.context)
        self.assertIn('client_secret', response.context)
        self.assertNotIn('save_info', self.client.session)
        self.assertNotIn('bag', self.client.session)

    def test_checkout_view_post_valid_form(self):
        # Create a session with some bag items
        self.client.post(
            reverse('add_to_bag', args=[product_id]), {'quantity': 1}
            )
        session = self.client.session
        session['bag'] = {'1': 1}
        session.save()

        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'New York',
            'street_address1': '123 Street',
            'street_address2': 'Apt 4',
            'county': 'NY',
            'save_info': False,
        }

        response = self.client.post(reverse('checkout'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse(
                             'checkout_success',
                             args=[Order.objects.last().order_number]
                              )
                )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Order successfully processed! Your order number is 1. \
            A confirmation email will be sent to john@example.com.'
            )

    def test_checkout_view_post_invalid_form(self):
        # Create a session with some bag items
        self.client.post(
            reverse('add_to_bag', args=[product_id]), {'quantity': 1}
            )
        session = self.client.session
        session['bag'] = {'1': 1}
        session.save()

        form_data = {
            'full_name': '',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'New York',
            'street_address1': '123 Street',
            'street_address2': 'Apt 4',
            'county': 'NY',
            'save_info': False,
        }

        response = self.client.post(reverse('checkout'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIn('stripe_public_key', response.context)
        self.assertIn('client_secret', response.context)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'There was an error with your form\
                . Please double check your information.')

    def test_checkout_view_get_empty_bag(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "There's nothing in your bag at the moment"
            )

    def test_checkout_view_missing_stripe_public_key(self):
        settings.STRIPE_PUBLIC_KEY = ''
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertNotIn('stripe_public_key', response.context)
        self.assertIn('client_secret', response.context)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Stripe public key is missing. \
            Did you forget to set it in your environment?'
            )
