import unittest
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Avatar
from checkout.models import Order
from .views import profile, edit_avatar, delete_avatar, order_history


class ProfileViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user)
        self.avatar = Avatar.objects.create(user=self.user)
        self.order = Order.objects.create(order_number='12345')

    def test_profile_view(self):
        url = reverse('profile')
        request = self.factory.get(url)
        request.user = self.user
        response = profile(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_edit_avatar_view(self):
        url = reverse('edit_avatar')
        request = self.factory.get(url)
        request.user = self.user
        response = edit_avatar(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_avatar.html')

    def test_delete_avatar_view(self):
        url = reverse('delete_avatar')
        request = self.factory.get(url)
        request.user = self.user
        response = delete_avatar(request)

        self.assertEqual(response.status_code, 302)
        # Redirects to profile view

    def test_order_history_view(self):
        order_number = self.order.order_number
        url = reverse('order_history', args=[order_number])
        request = self.factory.get(url)
        request.user = self.user
        response = order_history(request, order_number)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context_data['order'], self.order)
        self.assertTrue(response.context_data['from_profile'])


if __name__ == '__main__':
    unittest.main()
