from django.test import TestCase
from .models import Discount, Brand, Category, Product

class DiscountTestCase(TestCase):
    def setUp(self):
        # ایجاد یک تخفیف برای تست
        self.discount_percentage = Discount.objects.create(name='Test DiscountP', discount_type='percentage', value=10)
        self.discount_amount = Discount.objects.create(name='Test DiscountA', discount_type='amount', value=1000)



        # ایجاد یک دسته بندی برای تست
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # ایجاد یک محصول برای تست


class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Brand1', slug='test-brand')

    def test_str(self):
        self.assertEqual(self.brand, self.brand.name)

class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
    def test_str(self):
        self.assertEqual(self.category, self.category.name)

class ProductTestCase(TestCase):
    def setUp(self):

        self.product1 = Product.objects.create(
            name='Test Product',
            price=10000,
            quantity=10,
            main_image=None,  # این بخش را با تصویر معتبر تغییر دهید
            category=self.category,
            brand=self.brand,
            discount=self.discount_amount,
            discounted_price=None  # این بخش را با مقدار مناسب تغییر دهید
        )
        self.product2 = Product.objects.create(
            name='Test Product',
            price=10000,
            quantity=10,
            main_image=None,  # این بخش را با تصویر معتبر تغییر دهید
            category=self.category,
            brand=self.brand,
            discount=self.discount_percentage,
            discounted_price=None  # این بخش را با مقدار مناسب تغییر دهید
        )
        # تست اعتبارسنجی مدل محصول
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.brand, self.brand)
        self.assertEqual(product.discount, self.discount)
        # ادامه تست موارد دیگر
    def test_discount_model(self):
        # تست اعتبارسنجی مدل تخفیف
        discount = Discount.objects.get(code='TESTCODE')
        self.assertEqual(discount.discount_type, 'percentage')
        self.assertEqual(discount.value, 20)

    def test_brand_model(self):
        # تست اعتبارسنجی مدل برند
        brand = Brand.objects.get(name='Test Brand')
        self.assertEqual(brand.name, 'Test Brand')

    def test_category_model(self):
        # تست اعتبارسنجی مدل دسته بندی
        category = Category.objects.get(name='Test Category')
        self.assertEqual(category.name, 'Test Category')
    # افزودن تست‌های دیگر به میزان نیاز