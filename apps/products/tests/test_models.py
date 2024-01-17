# aaaaaaaaaaa
from django.test import TestCase
from ..models import Discount, Brand, Category, Product, Comment, Like
from ...accounts.models import User


class DiscountTestCase(TestCase):
    def setUp(self):
        self.discount_percentage = Discount.objects.create(code='Test DiscountP', discount_type='percentage', value=10)
        self.discount_amount = Discount.objects.create(code='Test DiscountA', discount_type='amount', value=100)

    def test_discount_p_model(self):
        discount = Discount.objects.get(code='Test DiscountP')
        self.assertEqual(discount.discount_type, 'percentage')
        self.assertEqual(discount.value, 10)
        self.assertEqual(discount.code, 'Test DiscountP')

    def test_discount_a_model(self):
        discount = Discount.objects.get(code='Test DiscountA')
        self.assertEqual(discount.discount_type, 'amount')
        self.assertEqual(discount.value, 100)
        self.assertEqual(discount.code, 'Test DiscountA')


class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(
            name='Test Brand',
            slug='test-brand',
            description='ghashang',
            image=None,
        )

    def test_brand_model(self):
        brand = Brand.objects.get(name='Test Brand')
        self.assertEqual(brand.name, 'Test Brand')
        self.assertEqual(brand.slug, 'test-brand')
        self.assertEqual(brand.description, 'ghashang')


class CategoryTestCase(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(
            name='Parent Category',
            slug='parent-category',
            parent=None,
            image=None,
        )

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            parent=Category.objects.get(name='Parent Category'),
            image=None,
        )

    def test_category_model(self):
        category = Category.objects.get(name='Test Category')
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.slug, 'test-category')
        self.assertEqual(category.parent.name, 'Parent Category')


class ProductTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name='Test Product1',
            price=1000,
            quantity=10,
            main_image=None,
            category=Category.objects.create(
                name='Test Category',
                slug='test-category',
                parent=Category.objects.create(name='Parent Category',
                                               slug='parent-category',
                                               parent=None,
                                               image=None, ),
            ),
            brand=Brand.objects.create(
                name='Test Brand',
                slug='test-brand',
                description='ghashang',
                image=None,
            ),
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

class CommentModelTests(TestCase):
    def setUp(self):
        self.comment = Comment.objects.create(
            product = Product.objects.create(
                name='Test Comment',
                price=1000,
                quantity=10,
                main_image=None,
                category=Category.objects.create(name='Test Category2', slug='test-category-2'),
                brand=Brand.objects.create(name='Test Brand2', slug='test-brand-2'),
                discount=Discount.objects.create(code='Test DiscountA', discount_type='amount', value=100),
                discounted_price=None
            ),
            reply = None,
            author = User.objects.create(username='zeinab', first_name='zeinab', last_name='moghadamnia', email='zeinab@moghadamnia', phone_number='09032554304'),
            context = "saaaaaaaalaaaaaam",
        )
    def test_comment_model(self):
        comment = Comment.objects.get(author__email="zeinab@moghadamnia")
        self.assertEqual(comment.author.phone_number, '09032554304')
        self.assertEqual(comment.product.name, 'Test Comment')
        self.assertEqual(comment.context, "saaaaaaaalaaaaaam")

class LikeModelTest(TestCase):
    def setUp(self):
        self.like = Like.objects.create(
            product=Product.objects.create(
                name='Test Like',
                price=1000,
                quantity=10,
                main_image=None,
                category=Category.objects.create(name='Test Category2', slug='test-category-2'),
                brand=Brand.objects.create(name='Test Brand2', slug='test-brand-2'),
                discount=Discount.objects.create(code='Test DiscountA', discount_type='amount', value=100),
                discounted_price=None
            ),
            user=User.objects.create(username='zeinab', first_name='zeinab', last_name='moghadamnia',
                                       email='zeinab@moghadamnia', phone_number='09032554304'),
        )
    def test_like(self):
        like = Like.objects.get(product__name='Test Like')
        self.assertEqual(like.product.discount.discount_type, 'amount')
        self.assertEqual(like.user.phone_number, '09032554304')
