import ast
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import AddToCartSerializer, DeleteFromCartSerializer
from ...products.models import Product
from ...accounts.models import Address
import datetime
from django.shortcuts import render
from ..forms import AddressSelectionForm

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

    def select_address(request):
        user = request.user
        form = AddressSelectionForm(user=user)
        if request.method == 'POST':
            form = AddressSelectionForm(user=user, data=request.POST)
            if form.is_valid():
                selected_address_id = form.cleaned_data['address']
                selected_address = Address.objects.get(id=selected_address_id)
                return render(request, 'orders/success.html', {'selected_address': selected_address})
        return render(request, 'orders/select_address.html', {'form': form})


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
                    # expires = datetime.datetime.now() + datetime.timedelta(seconds=15)
                    # str_expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S')
                    # response.set_cookie('shopping_cart', json.dumps(shopping_cart), expires=str_expires)
                    return response
        return Response({'message': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)




