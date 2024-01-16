from django.test import TestCase
from ..models import Discount, Brand, Category, Product

class DiscountTestCase(TestCase):
    def setUp(self):
        self.discount_percentage = Discount.objects.create(code='Test DiscountP', discount_type='percentage', value=10)
        self.discount_amount = Discount.objects.create(code='Test DiscountA', discount_type='amount', value=100)


    def test_discount_p_model(self):
        discount = Discount.objects.get(code='Test DiscountP')
        self.assertEqual(discount.discount_type, 'percentage')
        self.assertEqual(discount.value, 10)
    def test_discount_a_model(self):
        discount = Discount.objects.get(code='Test DiscountA')
        self.assertEqual(discount.discount_type, 'amount')
        self.assertEqual(discount.value, 100)


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
            name='Test Product1',
            price=1000,
            quantity=10,
            main_image=None,
            category=Category.objects.create(name='Test Category', slug='test-category'),
            brand=Brand.objects.create(name='Test Brand', slug='test-brand'),
            discount=Discount.objects.create(code='Test DiscountP', discount_type='percentage', value=50),
            discounted_price=None
        )
        self.product2 = Product.objects.create(
            name='Test Product2',
            price=1000,
            quantity=10,
            main_image=None,
            category=Category.objects.create(name='Test Category2', slug='test-category-2'),
            brand=Brand.objects.create(name='Test Brand2', slug='test-brand-2'),
            discount=Discount.objects.create(code='Test DiscountA', discount_type='amount', value=100),
            discounted_price=None
        )
    def test_product1_model(self):
        product1 = Product.objects.get(name='Test Product1')
        self.assertEqual(product1.name, 'Test Product1')
        self.assertEqual(product1.price, 1000)
        self.assertEqual(product1.quantity, 10)
        self.assertEqual(product1.category.name, 'Test Category')
        self.assertEqual(product1.brand.name, 'Test Brand')
        self.assertEqual(product1.discount.code, 'Test DiscountP')
        self.assertEqual(product1.discounted_price, 500)
    def test_product2_model(self):
        product2 = Product.objects.get(name='Test Product2')
        self.assertEqual(product2.name, 'Test Product2')
        self.assertEqual(product2.price, 1000)
        self.assertEqual(product2.quantity, 10)
        self.assertEqual(product2.category.name, 'Test Category2')
        self.assertEqual(product2.brand.name, 'Test Brand2')
        self.assertEqual(product2.discount.code, 'Test DiscountA')
        self.assertEqual(product2.discounted_price, 900)

