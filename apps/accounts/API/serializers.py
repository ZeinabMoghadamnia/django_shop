from rest_framework import serializers
from ..models import Address
from ...orders.models import Order, OrderItem
from ...products.models import Image


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'sub_image', 'is_main']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'discount', 'product_name', 'product_image', 'product_price']

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_price(self, obj):
        if obj.product.discounted_price:
            return obj.product.discounted_price
        else:
            return obj.product.price

    def get_product_image(self, obj):
        try:
            main_image = obj.product.image.filter(is_main=True).first()
            if main_image:
                return ImageSerializer(main_image).data
            else:
                return None
        except AttributeError:
            return None



class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'user', 'postal_code', 'province', 'city', 'complete_address']

