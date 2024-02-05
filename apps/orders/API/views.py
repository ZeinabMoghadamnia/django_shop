from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django_shop.apps.orders.API.serializers import AddToCartSerializer  # Import your serializer here
from django_shop.apps.products.models import Product
import datetime

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

        product_id = serializer.validated_data['product_id']  # Fix: Correct field name
        order_quantity = serializer.validated_data['quantity']
        name = serializer.validated_data['name']
        price = serializer.validated_data['price']
        discounted_price = serializer.validated_data.get('discounted_price', None)  # Fix: Handle optional field

        product = Product.objects.get(id=product_id)

        if product.quantity >= order_quantity:
            price = discounted_price if discounted_price is not None else price
            item = {'product_id': product_id, 'quantity': order_quantity, 'name': name, 'price': price}

            shopping_cart = request.COOKIES.get('shopping_cart', '')
            shopping_cart += f';{item}'  # Fix: Correct string formatting

            response = Response({'shopping_cart': 'ok'})
            expires = datetime.datetime.now() + datetime.timedelta(hours=5)
            str_expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S')
            response.set_cookie('shopping_cart', shopping_cart, expires=str_expires)
            return response
        else:
            return Response({'message': 'not enough'}, status=status.HTTP_400_BAD_REQUEST)
