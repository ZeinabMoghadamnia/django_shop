from django.test import TestCase
from ..models import Discount, Brand, Category, Product

class DiscountTestCase(TestCase):
    def setUp(self):
        self.discount_percentage = Discount.objects.create(name='Test DiscountP', discount_type='percentage', value=10)
        self.discount_amount = Discount.objects.create(name='Test DiscountA', discount_type='amount', value=1000)


    def test_discount_model(self):
        discount = Discount.objects.get(code='TESTCODE')
        self.assertEqual(discount.discount_type, 'percentage')
        self.assertEqual(discount.value, 20)


class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Test Brand', slug='tests-brand')

    def test_brand_model(self):
        brand = Brand.objects.get(name='Test Brand')
        self.assertEqual(brand.name, 'Test Brand')

class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='tests-category')

    def test_category_model(self):
        category = Category.objects.get(name='Test Category')
        self.assertEqual(category.name, 'Test Category')

class ProductTestCase(TestCase):
    def setUp(self):

        self.product1 = Product.objects.create(
            name='Test Product',
            price=10000,
            quantity=10,
            main_image=None,
            category=self.category,
            brand=self.brand,
            discount=self.discount_amount,
            discounted_price=None
        )
        self.product2 = Product.objects.create(
            name='Test Product',
            price=10000,
            quantity=10,
            main_image=None,
            category=self.category,
            brand=self.brand,
            discount=self.discount_percentage,
            discounted_price=None
        )
    def test_product_model(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.category, self.product1.category)
        self.assertEqual(product.brand, self.product1.brand)
        self.assertEqual(product.discount, self.product1.discount)
