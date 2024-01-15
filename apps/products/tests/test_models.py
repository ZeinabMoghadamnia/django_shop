from django.test import TestCase
from ..models import Discount, Brand, Category, Product

class DiscountTestCase(TestCase):
    def setUp(self):
        self.discount_percentage = Discount.objects.create(code='Test DiscountP', discount_type='percentage', value=10)
        self.discount_amount = Discount.objects.create(code='Test DiscountA', discount_type='amount', value=1000)


    def test_discount_model(self):
        discount = Discount.objects.get(code='Test DiscountP')
        self.assertEqual(discount.discount_type, 'percentage')
        self.assertEqual(discount.value, 10)


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
        self.product = Product.objects.create(
            name='Test Product1',
            price=1000,
            quantity=10,
            main_image=None,  # این بخش را با تصویر معتبر تغییر دهید
            category=Category.objects.create(name='Test Category', slug='test-category'),
            brand=Brand.objects.create(name='Test Brand', slug='test-brand'),
            discount=Discount.objects.create(code='Test DiscountP', discount_type='percentage', value=20),
            discounted_price=None  # این بخش را با مقدار مناسب تغییر دهید
        )
        # self.product2 = Product.objects.create(
        #     name='Test Product2',
        #     price=10000,
        #     quantity=10,
        # )
    def test_product_model(self):
        product = Product.objects.get(name='Test Product1')
        self.assertEqual(product.name, 'Test Product1')
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.category.name, 'Test Category')  # تغییر در اینجا
        self.assertEqual(product.brand.name, 'Test Brand')  # تغییر در اینجا
        self.assertEqual(product.discount.code, 'Test DiscountP')  # تغییر در اینجا

