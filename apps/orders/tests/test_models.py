from django.test import TestCase
from django_shop.apps.accounts.models import User
from django_shop.apps.orders.models import Order, OrderItem
from django_shop.apps.products.models import Product, Category, Brand, Discount

class OrderItemModelTest(TestCase):

    def setUp(self):
        self.order_item = OrderItem.objects.create(
            product = Product.objects.create(
                name='Test Product1',
                price=1000,
                quantity=10,
                category=Category.objects.create(name='Test Category', slug='test-category'),
                brand=Brand.objects.create(name='Test Brand', slug='test-brand'),
            ),

            quantity = 2,
            is_paid=False,
        )

    def test_order_item_str(self):
        order_item = OrderItem.objects.get(product__name='Test Product1')
        self.assertEqual(self.order_item.product.category.name, 'Test Category')
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.is_paid, False)

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            user = User.objects.create_user(username='zeinab', first_name='zeinab', last_name='moghadamnia', email='zeinab@moghadamnia', phone_number='09001112233'),
            items = OrderItem.objects.create(
                product = Product.objects.create(
                    name='Test Product1',
                    price=1000,
                    quantity=10,
                    category=Category.objects.create(name='Test Category', slug='test-category'),
                    brand=Brand.objects.create(name='Test Brand', slug='test-brand'),
                ),
                quantity=2,
                is_paid=False,
            ),
            total_price= 2000,
        )
    def test_order_model(self):
        order = Order.objects.get(user__first_name='zeinab')
        self.assertEqual(order.user.email, 'zeinab@moghadamnia')
        self.assertEqual(order.items.product.name, 'Test Product1')
        self.assertEqual(order.items.quantity, 2)
        self.assertEqual(order.total_price, 2000)

