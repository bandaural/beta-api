"""
Serializers for supplier apis.
"""

from rest_framework import serializers

from core.models import Category, Supplier

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SupplierSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Supplier
        fields =['id', 'name', 'category']

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
        supplier = Supplier.objects.get_or_create(
                                            user = auth_user,
                                            category=category,
                                            **supplier_data)
        print(supplier)
        return supplier

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        print(validated_data)

        request = self.context.get('request')
        auth_user = request.user
        print(auth_user)

        category, created = Category.objects.get_or_create(
                                            user = auth_user,
                                            **category_data
        )
        print(category)


        name = instance.name
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance