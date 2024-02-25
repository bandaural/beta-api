"""
Tests for the Django Admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create a user and client for tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@admin.com',
            password='12345678'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='12345678',
            name='User name'
        )

    def test_users_list(self):
        """Test that users are listed on page. """
        url = reverse('admin:core_user_changelist') #Documentation https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

