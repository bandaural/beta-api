"""
Serializers for recipes APIs.
"""

from rest_framework import serializers

from core.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transactions. """

    class Meta:
        model = Transaction
        fields = ['id', 'card', 'income', 'expense', 'currency', 'date', 'type', 'comment', 'billing_month', 'category', 'supplier']
        read_only_fields = ['id']


class TransactionDetailSerializer(TransactionSerializer):
    """Serializer for the detail of transaction"""

    class Meta(TransactionSerializer.Meta):
        fields = TransactionSerializer.Meta.fields

