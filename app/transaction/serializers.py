"""
Serializers for recipes APIs.
"""

from rest_framework import serializers

from core.models import Transaction, Category, Supplier, Body
from rest_framework.fields import CurrentUserDefault


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ['id', 'description']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields =['id', 'name', 'category']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transactions. """
    category = CategorySerializer()
    supplier = SupplierSerializer()
    class Meta:
        model = Transaction
        fields = ['id',
                 'card',
                 'income',
                 'expense',
                 'currency',
                 'date',
                 'type',
                 'comment',
                 'billing_month',
                 'category',
                 'supplier']
        read_only_fields = ['id']


    def create(self, validated_data):
        category_data = validated_data.pop('category')
        print(category_data)

        request = self.context.get('request')
        auth_user = request.user
        print(auth_user)

        category, created = Category.objects.get_or_create(
                                            user = auth_user,
                                            **category_data)
        print(category)

        supplier_data = validated_data.pop('supplier', [])
        print(supplier_data)
        supplier, created = Supplier.objects.get_or_create(
                                            user = auth_user,
                                            category=category,
                                            **supplier_data)
        print(supplier)
        print(validated_data)
        transaction = Transaction.objects.create(
                                    category=category,
                                    supplier=supplier,
                                    **validated_data)
        print(transaction)
        return transaction

    def update(self, validated_data):

        pass



