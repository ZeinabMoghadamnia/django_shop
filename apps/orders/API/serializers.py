from rest_framework import serializers
from ..models import Order, OrderItem

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField(min_value=0)
    discounted_price = serializers.IntegerField(min_value=0)

class DeleteFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

# class DeleteFromCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

