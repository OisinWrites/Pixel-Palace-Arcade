from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Product, Category
from .forms import ProductForm
from blog.models import Rating, Review
from profiles.models import Avatar


class ProductViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.category = Category.objects.create(name='Category')

        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            category=self.category,
            price=10.0,
            image='test_image.jpg',
        )

    def test_all_products_view(self):
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertIn('products', response.context)
        self.assertIn('search-term', response.context)
        self.assertIn('current_categories', response.context)
        self.assertIn('current_sorting', response.context)

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('product_detail', args=[self.product.id])
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertIn('form', response.context)
        self.assertIn('rating', response.context)
        self.assertIn('product', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('avatars', response.context)

    def test_add_product_view_authenticated_superuser(self):
        self.client.login(username='admin', password='adminpassword')

        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
            )

        form_data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'category': self.category.id,
            'price': 20.0,
            'image': image,
        }

        response = self.client.post(
            reverse('add_product'), data=form_data, follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertIn('form', response.context)
        self.assertIn('rating', response.context)
        self.assertIn('product', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('avatars', response.context)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Successfully added product!')

    def test_add_product_view_authenticated_non_superuser(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.'
            )

    def test_edit_product_view_authenticated_superuser(self):
        self.client.login(username='admin', password='adminpassword')

        form_data = {
            'name': 'Updated Product',
            'description': 'This is an updated product',
            'category': self.category.id,
            'price': 15.0,
        }

        response = self.client.post(
            reverse('edit_product', args=[self.product.id]),
            data=form_data, follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertIn('form', response.context)
        self.assertIn('rating', response.context)
        self.assertIn('product', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('avatars', response.context)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Successfully updated product!')

    def test_edit_product_view_authenticated_non_superuser(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(
            reverse('edit_product', args=[self.product.id])
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.'
            )

    def test_delete_product_view_authenticated_superuser(self):
        self.client.login(username='admin', password='adminpassword')

        response = self.client.post(
            reverse('delete_product', args=[self.product.id]), follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product deleted!')

    def test_delete_product_view_authenticated_non_superuser(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(
            reverse('delete_product', args=[self.product.id])
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.'
            )
