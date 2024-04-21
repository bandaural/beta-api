"""
Views for the recipe APIs.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Transaction, Supplier, Category
from .serializers import SupplierSerializer

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def supplier(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.filter(user=request.user)
        serializer = SupplierSerializer(suppliers, many = True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def supplier_detail(request, id):

    try:
        supplier = Supplier.objects.get(pk=id)
    except Supplier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SupplierSerializer(supplier, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

