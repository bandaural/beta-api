"""
Views for the recipe APIs.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Transaction, Supplier, Category, Body
from .serializers import TransactionSerializer, BodySerializer
from .aux import transform_body


from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transaction(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many = True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        print(request.data)
        category = request.data.get('category')
        print(category)
        print(request.user)
        #Si la transacción no llega con el campo categoría
        if category == None:
            print('POST sin categoria')
            data = request.data

            #Revisar si el supplier de la transacción existir la categoría del supplier
            name_supplier = data['supplier']
            supplier_exists = Supplier.objects.filter(user=request.user, name=name_supplier['name']).exists()
            print(supplier_exists)
            if supplier_exists == True:
                queryset = Supplier.objects.filter(user=request.user, name=name_supplier['name']).values('id', 'name', 'category')
                print(queryset)
                queryset_data = list(queryset)

                category = Category.objects.filter(id=queryset_data[0]['category']).values('name')
                category_name = list(category)[0]['name']
                supplier_category = {
                    "name": category_name
                }
                data['category'] = supplier_category
                print(data)
                transaction_serializer = TransactionSerializer(data=data, context={'request': request})
                print(transaction_serializer)

                if transaction_serializer.is_valid():
                    transaction_serializer.save(user=request.user)
                    return Response(transaction_serializer.data, status = status.HTTP_201_CREATED)

            #Si no existe el supplier se usa la categoría "pendiente"
            else:
                print('Sin categoría')
                category = {
                    "name": "Pending"
                }
                data['category'] = category
                print(data)
                transaction_serializer = TransactionSerializer(data=data, context={'request': request})
                if transaction_serializer.is_valid():
                    transaction_serializer.save(user=request.user)
                    return Response(transaction_serializer.data, status = status.HTTP_201_CREATED)

        else:
            print('aqui estamos')
            data = request.data
            #data['user'] = request.user.id
            print(data)
            transaction_serializer = TransactionSerializer(data=data, context={'request': request})

            if transaction_serializer.is_valid():
                transaction_serializer.save(user=request.user)
                return Response(transaction_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transaction_detail(request, id):

    try:
        transaction = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def body(request):
    if request.method == 'GET':
        bodies = Body.objects.filter(user=request.user)
        serializer = BodySerializer(bodies, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        body_serializer = BodySerializer(data=request.data)
        if body_serializer.is_valid():
            body_serializer.save(user=request.user)

            body = str(body_serializer['description'])
            print(body)
            dict = transform_body(body)
            print(dict)
            data = dict

            #Revisar si el supplier de la transacción existir la categoría del supplier
            name_supplier = data['supplier']
            supplier_exists = Supplier.objects.filter(user=request.user, name=name_supplier['name']).exists()
            print(supplier_exists)
            if supplier_exists == True:
                queryset = Supplier.objects.filter(user=request.user, name=name_supplier['name']).values('id', 'name', 'category')
                print(queryset)
                queryset_data = list(queryset)

                category = Category.objects.filter(id=queryset_data[0]['category']).values('name')
                category_name = list(category)[0]['name']
                supplier_category = {
                    "name": category_name
                }
                data['category'] = supplier_category
                print(data)
                transaction_serializer = TransactionSerializer(data=data, context={'request': request})
                print(transaction_serializer)

                if transaction_serializer.is_valid():
                    transaction_serializer.save(user=request.user)
                    return Response(transaction_serializer.data, status = status.HTTP_201_CREATED)

            #Si no existe el supplier se usa la categoría "pendiente"
            else:
                category = {
                    "name": "Pending"
                }
                data['category'] = category
                print(data)
                transaction_serializer = TransactionSerializer(data=data, context={'request': request})
                if transaction_serializer.is_valid():
                    transaction_serializer.save(user=request.user)
                    return Response(transaction_serializer.data, status = status.HTTP_201_CREATED)






