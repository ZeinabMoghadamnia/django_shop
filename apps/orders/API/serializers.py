from rest_framework import serializers

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField(min_value=0)
    # discounted_price = serializers.IntegerField(min_value=0)

class DeleteFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


