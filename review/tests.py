from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from products.models import Product
from blog.models import Review


class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10)

    def test_create_review(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('create_review', args=[self.product.pk])
        data = {'content': 'Great product'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail',
                              kwargs={'product_id': self.product.pk}))

        # Verify that the review is created
        review = Review.objects.filter(
            product=self.product, user=self.user).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.content, 'Great product')

        # Verify that the success message is displayed
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
            ]
        self.assertIn('New review added', messages)

    def test_update_review(self):
        self.client.login(username='testuser', password='testpassword')
        review = Review.objects.create(
            product=self.product, user=self.user, content='Initial content'
            )
        url = reverse('update_review', args=[review.pk])
        data = {'content': 'Updated content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail',
                              kwargs={'product_id': self.product.pk})
            )

        # Verify that the review is updated
        review.refresh_from_db()
        self.assertEqual(review.content, 'Updated content')

    def test_delete_review(self):
        self.client.login(username='testuser', password='testpassword')
        review = Review.objects.create(
            product=self.product, user=self.user, content='Test review'
            )
        url = reverse('delete_review', args=[review.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail',
                              kwargs={'product_id': self.product.pk})
            )

        # Verify that the review is deleted
        review_exists = Review.objects.filter(pk=review.pk).exists()
        self.assertFalse(review_exists)

        # Verify that the success message is displayed
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
            ]
        self.assertIn('Review deleted!', messages)
