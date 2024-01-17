from django.test import TestCase
from ..models import Order, OrderItem
from ...products.models import Product


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            product = Product.objects.create(
            name = 'Test Product',
            price = 1000,

            )
        )

        self.quantity = 1,