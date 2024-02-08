import ast
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import AddToCartSerializer, DeleteFromCartSerializer
from ...products.models import Product
import datetime
from django.shortcuts import render

# class AddToCartSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField()
#     name = serializers.CharField()
#     quantity = serializers.IntegerField()
#     price = serializers.IntegerField(min_value=0)
#     discounted_price = serializers.IntegerField(min_value=0, required=False)

class AddToCartView(APIView):
    serializer_class = AddToCartSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get('product_id')
        quantity = serializer.validated_data.get('quantity')
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        discounted_price = serializer.validated_data.get('discounted_price')

        product = Product.objects.get(id=product_id)
        if product.quantity >= 0:
            price = discounted_price if discounted_price is not None else price
            item = {'product_id': product_id, 'quantity': quantity, 'name': name, 'price': price}

            shopping_cart = request.COOKIES.get('shopping_cart')

            if shopping_cart:
                shopping_cart = json.loads(shopping_cart)
            else:
                shopping_cart = []

            shopping_cart.append(item)

            response = Response({'shopping_cart': 'ok'})
            # expires = datetime.datetime.now() + datetime.timedelta(seconds=15)
            # str_expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S')

            # response.set_cookie('shopping_cart', json.dumps(shopping_cart), expires=str_expires)
            response.set_cookie('shopping_cart', json.dumps(shopping_cart))
            return response
        else:
            return Response({'message': 'not enough'}, status=status.HTTP_400_BAD_REQUEST)

class ShoppingCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        shopping_cart = request.COOKIES.get('shopping_cart')
        if shopping_cart:
            shopping_cart = json.loads(shopping_cart)
        else:
            shopping_cart = []
        # print(type(shopping_cart))
        # Return JSON response
        return render(request, "orders/shopping_cart.html", {'shopping_cart': shopping_cart})


# class AddToCartView(APIView):
#     serializer_class = AddToCartSerializer
#     permission_classes = [AllowAny]
#     list_cart = []
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         product_id = serializer.validated_data.get('product_id')
#         # quantity = serializer.validated_data.get('order_quantity')
#         quantity = 1
#         name = serializer.validated_data.get('name')
#         price = serializer.validated_data.get('price')
#         discounted_price = serializer.validated_data.get('discounted_price')
#
#         product = Product.objects.get(id=product_id)
#         if product.quantity >= 0:
#             price = discounted_price if discounted_price is not None else price
#             # item = {'product_id': product_id, 'name': name, 'price': price}
#             item = {'product_id': product_id, 'quantity': quantity, 'name': name.encode('utf-8'), 'price': price}
#             shopping_cart = request.COOKIES.get('shopping_cart')
#             self.list_cart.append(shopping_cart)
#             self.list_cart.append(item)
#             # shopping_cart += f';{item}'  # Fix: Correct string formatting
#
#             response = Response({'shopping_cart': 'ok'})
#             expires = datetime.datetime.now() + datetime.timedelta(hours=5)
#             str_expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S')
#             response.set_cookie('shopping_cart', self.list_cart, expires=str_expires)
#             print(shopping_cart)
#             return response
#         else:
#             return Response({'message': 'not enough'}, status=status.HTTP_400_BAD_REQUEST)

class DeleteFromCartView(APIView):
    serializer_class = DeleteFromCartSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get('product_id')

        shopping_cart = request.COOKIES.get('shopping_cart')
        if shopping_cart:
            shopping_cart = json.loads(shopping_cart)
            for item in shopping_cart:
                if item['product_id'] == product_id:
                    shopping_cart.remove(item)
                    response = Response({'message': 'Item removed from cart'})
                    expires = datetime.datetime.now() + datetime.timedelta(hours=5)
                    str_expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S')
                    response.set_cookie('shopping_cart', json.dumps(shopping_cart), expires=str_expires)
                    return response
        return Response({'message': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)




