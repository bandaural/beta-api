"""
Tests for transaction APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Transaction

from transaction.serializers import TransactionSerializer


TRANSACTIONS_URL = reverse('transaction:transaction-list')

def create_transaction(user, **params):
    """Create and return a sample transaction. """
    defaults = {
        'card' : '',
        'income': 4124,
        'currency': 'CLP',
        'type': 'credit',
        'comment': 'weed',
        'billing_month': 'june'
    }
    defaults.update(params)
    transaction = Transaction.objects.create(user=user, **defaults)
    return transaction


class PublicTransactionAPITest(TestCase):
    """Test unauthenticated API request."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_transactions(self):
        """Test retrieving a list of transactions."""
        create_transaction(user=self.user)
        create_transaction(user=self.user)

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by('-id')
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_transactions_list_limited_to_user(self):
        """Test list of transactions is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_transaction(user=other_user)
        create_transaction(user=self.user)

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.filter(user=self.user)
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)