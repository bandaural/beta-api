"""
Views for the recipe APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Transaction
from transaction import serializers



class TransactionViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.TransactionDetailSerializer
    queryset = Transaction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve transaction for authenticated user. """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TransactionSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new transaction."""
        serializer.save(user=self.request.user)