import ast
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import AddToCartSerializer, DeleteFromCartSerializer
from ...accounts.API.serializers import OrderSerializer
from ...products.models import Product, Discount
from ...accounts.models import Address
from ...orders.models import Order, OrderItem
import datetime
from django.shortcuts import render, get_object_or_404
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
            # If user is authenticated, save data in database
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(user=request.user, status='processing', is_paid=False)

                order_item, item_created = OrderItem.objects.get_or_create(order=order, product_id=product_id, defaults={'quantity': quantity})
                if not item_created:
                    order_item.quantity += quantity
                    order_item.save()

                order_items = order.orders.all()
                total_price = sum(item.product.price * item.quantity for item in order_items)
                order.total_price = total_price
                order.save()
                return Response({'message': 'Product added to cart successfully'})

            # If user is not authenticated, save data in session
            else:
                price = discounted_price if discounted_price is not None else price
                item = {'product_id': product_id, 'quantity': quantity, 'name': name, 'price': price}

                shopping_cart = request.COOKIES.get('shopping_cart')

                if shopping_cart:
                    shopping_cart = json.loads(shopping_cart)
                else:
                    shopping_cart = []

                shopping_cart.append(item)

                response = Response({'shopping_cart': 'ok'})
                response.set_cookie('shopping_cart', json.dumps(shopping_cart))
                return response

        else:
            return Response({'message': 'Not enough quantity available'}, status=status.HTTP_400_BAD_REQUEST)




class ShoppingCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_orders = Order.objects.filter(user=request.user, status='processing', is_paid=False)
            shopping_cart = []
            for order in user_orders:
                order_items = order.orders.all()
                for item in order_items:
                    shopping_cart.append({'product_id': item.product_id, 'name': item.product.name, 'quantity': item.quantity, 'price': item.product.price})
        else:
            shopping_cart = request.COOKIES.get('shopping_cart')
            if shopping_cart:
                shopping_cart = json.loads(shopping_cart)
            else:
                shopping_cart = []
            # print(type(shopping_cart))
            # Return JSON response
        return render(request, "orders/shopping_cart.html", {'shopping_cart': shopping_cart})

    def select_address(self, request):
        user = request.user
        form = AddressSelectionForm(user=user)
        if request.method == 'POST':
            form = AddressSelectionForm(user=user, data=request.POST)
            if form.is_valid():
                selected_address_id = form.cleaned_data['address']
                selected_address = Address.objects.get(id=selected_address_id)
                return render(request, 'orders/order_registration_result.html', {'selected_address': selected_address})
        return render(request, 'orders/select_address.html', {'form': form})


class DeleteFromCartView(APIView):
    # serializer_class = DeleteFromCartSerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            # If user is authenticated, delete from database
            user_orders = Order.objects.filter(user=request.user, status='processing', is_paid=False)
            for order in user_orders:
                order_items = order.orders.all()
                for item in order_items:
                    print(item.id)
                    if item.product.id == kwargs.get('product_id'):  # Assuming the URL parameter is 'item_id'
                        item.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # If user is not authenticated, delete from cookie
            shopping_cart = request.COOKIES.get('shopping_cart')
            if shopping_cart:
                shopping_cart = json.loads(shopping_cart)
                for item in shopping_cart:
                    if item['id'] == kwargs.get('product_id'):
                        shopping_cart.remove(item)
                        response = Response(status=status.HTTP_204_NO_CONTENT)
                        response.set_cookie('shopping_cart', json.dumps(shopping_cart))
                        return response

        return Response({"error": "Item not found or unable to delete"}, status=status.HTTP_404_NOT_FOUND)


class UpdateCartItemView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, product_id, *args, **kwargs):
        quantity = request.data.get('quantity')
        if request.user.is_authenticated:
            order_items = OrderItem.objects.filter(order__user=request.user, product_id=product_id, order__is_paid=False)
            if order_items.exists():
                for order_item in order_items:
                    order_item.quantity = quantity
                    order_item.save()
                return Response({'message': 'Quantity updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Authentication required to update quantity'},
                            status=status.HTTP_401_UNAUTHORIZED)


class ApplyDiscountView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        discount_code = request.data.get('discount_code')
        order = Order.objects.get(user=request.user, is_paid=False)
        try:
            discount = Discount.objects.get(code=discount_code, is_active=True)
            if discount and discount.code == discount_code:
            # if discount.code == discount_code:
                # Calculate discounted price
                if discount.discount_type == 'percentage':
                    order.total_price = order.total_price - ((discount.value / 100) * order.total_price)
                elif discount.discount_type == 'amount':
                    order.total_price = order.total_price - int(discount.value)

                print(order.total_price)
                order.save()
                discount.is_active = False
                discount.save()

                return Response({'total_price': order.total_price}, status=200)
            else:
                return Response({'error': 'Invalid discount code'}, status=400)
        except:
            return JsonResponse({'message': 'Invalid discount code'})




class PaymentConfirmationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, status='processing', is_paid=False)
            order_items = OrderItem.objects.filter(order=order)

            for item in order_items:
                product = item.product
                quantity_in_cart = item.quantity
                if product.quantity < quantity_in_cart:
                    messages.error(request,  f"موجودی {product.name} کافی نیست.")
                    return render(request, 'orders/order_registration_result.html')
                    # error_message = f"موجودی {product.name} کافی نیست."
                    # return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            # اگر تمامی محصولات موجود بودند، سفارش ثبت شود
            for item in order_items:
                product = item.product
                quantity_in_cart = item.quantity
                product.quantity -= quantity_in_cart
                product.save()

            addres_id = request.data.get('address')
            address = Address.objects.get(id=addres_id)
            order.address = f"{address.province} - {address.city} - {address.complete_address}."
            order.is_paid = True
            order.save()
            messages.success(request, f"سفارش شما با موفقیت ثبت شد.")
            return render(request, 'orders/order_registration_result.html', {'order': order})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class DeleteFromCartView(APIView):
#     serializer_class = DeleteFromCartSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         product_id = serializer.validated_data.get('product_id')
#
#         shopping_cart = request.COOKIES.get('shopping_cart')
#         if shopping_cart:
#             shopping_cart = json.loads(shopping_cart)
#             for item in shopping_cart:
#                 if item['product_id'] == product_id:
#                     shopping_cart.remove(item)
#                     response = Response({'message': 'Item removed from cart'})
#                     # expires = datetime.datetime.now() + datetime.timedelta(seconds=15)
#                     # str_expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S')
#                     # response.set_cookie('shopping_cart', json.dumps(shopping_cart), expires=str_expires)
#                     return response
#         return Response({'message': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)




