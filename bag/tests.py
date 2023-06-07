from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product


class BagViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10)

    def test_view_bag(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        url = reverse('add_to_bag', args=[self.product.pk])
        data = {'quantity': 2, 'redirect_url': reverse('view_bag')}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_bag'))

        # Verify that the product is added to the bag
        bag = self.client.session.get('bag', {})
        self.assertEqual(len(bag), 1)
        self.assertEqual(bag[str(self.product.pk)], 2)

    def test_adjust_bag(self):
        # Add a product to the bag
        self.client.post(
            reverse('add_to_bag', args=[self.product.pk]),
            {'quantity': 1, 'redirect_url': reverse('view_bag')}
            )

        url = reverse('adjust_bag', args=[self.product.pk])
        data = {'quantity': 3}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_bag'))

        # Verify that the quantity of the product in the bag is adjusted
        bag = self.client.session.get('bag', {})
        self.assertEqual(len(bag), 1)
        self.assertEqual(bag[str(self.product.pk)], 3)

    def test_remove_from_bag(self):
        # Add a product to the bag
        self.client.post(
            reverse('add_to_bag', args=[self.product.pk]),
            {'quantity': 1, 'redirect_url': reverse('view_bag')}
            )

        url = reverse('remove_from_bag', args=[self.product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # Verify that the product is removed from the bag
        bag = self.client.session.get('bag', {})
        self.assertEqual(len(bag), 0)
