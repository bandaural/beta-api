"""
Serializers for recipes APIs.
"""

from rest_framework import serializers

from core.models import Category, Supplier, User
from rest_framework.fields import CurrentUserDefault


class CategorySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'user_id']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # Get the user making the request
        user = self.context['request'].user
        validated_data['user'] = user
        return super().update(instance, validated_data)


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class SupplierSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer()
    class Meta:
        model = Supplier
        fields =['id', 'name', 'category']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        """Update a supplier"""

        category_data = validated_data.pop('category', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if category_data:
            category_instance = instance.category

            # Check if category exists
            category_name = category_data.get('name')
            if category_instance and category_instance.name == category_name:
                category_serializer = CategorySerializer(instance=category_instance, data=category_data)
            else:
                # Create a new category instance
                user_id = self.context['request'].user.id
                category_data['user_id'] = user_id  # Assign the user ID to the category data
                category_serializer = CategorySerializer(data=category_data)

            if category_serializer.is_valid():
                category_instance = category_serializer.save()
                instance.category = category_instance
            else:
                # Handle validation errors if necessary
                pass

        return instance







