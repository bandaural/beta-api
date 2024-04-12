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
        'comment': 'weed'
    }
    defaults.update(params)
    transaction = Transaction.objects.create(user=user, **defaults)
    return transaction