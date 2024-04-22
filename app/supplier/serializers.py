"""
Serializers for recipes APIs.
"""

from rest_framework import serializers

from core.models import Transaction, Category, Supplier
from rest_framework.fields import CurrentUserDefault


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class SupplierSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Supplier
        fields =['id', 'name', 'category']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        """Update a supplier"""

        category = validated_data.pop('category')
        print(category)


        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
