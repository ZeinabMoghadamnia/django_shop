from django.test import TestCase
from ..models import Order, OrderItem
from ...products.models import Product, Category, Brand, Discount
from ...accounts.models import User

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product1',
            price=1000,
            quantity=10,
            category=Category.objects.create(name='Test Category', slug='test-category'),
            brand=Brand.objects.create(name='Test Brand', slug='test-brand'),
            discount=Discount.objects.create(code='Test DiscountP', discount_type='percentage', value=50),
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            parent=Category.objects.get(name='Parent Category'),
        )
        self.brand = Brand.objects.create(
            name='Test Brand',
            slug='test-brand',
            description='ghashang',
        )
        self.discount = Discount.objects.create(
            code='Test DiscountP', discount_type='percentage', value=10,
            slug='test-discountp'
        )

        self.order = Order.objects.create(
            product=self.product,
            quantity=1,
            price=1000,
        )

    def test_order_model(self):
        order = Order.objects.get(product='Test Product1')
        self.assertEqual(order.product, 'Test Product1')
        self.assertEqual(order.quantity, 1)
        self.assertEqual(order.price, 1000)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='zeinab',
            email='zeinab@gmail.com',
            phone_number='09032554304',
            first_name='zeinab',
            last_name='moghadamnia',
        )

        self.items = OrderItem.objects.create(
            product='Test Product1',
            quantity=1,
            price=1000,
        )

        self.total_price = 1000

    def test_order_item_model(self):
        order_item = OrderItem.objects.get(user=self.user)
        self.assertEqual(order_item.user.username, 'zeinab')
        self.assertEqual(order_item.items.product, 'Test Product1')
        self.assertEqual(order_item.total_price, 1000)