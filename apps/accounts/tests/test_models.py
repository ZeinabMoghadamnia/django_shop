from datetime import datetime
from django.test import TestCase
from django_shop.apps.accounts.models import User, Address
from django.utils import timezone
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='zeinab',
            user_type = 'costumer',
            email = 'zeinab@gmail.com',
            phone_number = '09001112233',
            first_name = 'zeinab',
            last_name = 'moghadamnia',
            date_of_birth = '2002-07-23',
            image = None,
            is_active = True,
            is_deleted = False,
        )
    def test_user_model(self):
        user = User.objects.get(username='zeinab')
        self.assertEqual(user.username, 'zeinab')
        self.assertEqual(user.user_type, 'costumer')
        self.assertEqual(user.email, 'zeinab@gmail.com')
        self.assertEqual(user.phone_number, '09001112233')
        self.assertEqual(user.first_name, 'zeinab')
        self.assertEqual(user.last_name, 'moghadamnia')
        self.assertEqual(user.date_of_birth, datetime.strptime('2002-07-23', "%Y-%m-%d").date())
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_deleted, False)
class AddressModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            customer = User.objects.create(
                username='zeinab',
                email='zeinab@gmail.com',
                phone_number='09001112233',
                first_name='zeinab',
                last_name='moghadamnia',
            ),
            province = 'Tehran',
            city = 'Tehran',
            complete_address = 'Tehran, Tehran, khoone',
            is_active=True,
            is_deleted=False,
        )

    def test_address_model(self):
        address = Address.objects.get(province='Tehran')
        self.assertEqual(address.customer.email, 'zeinab@gmail.com')
        self.assertEqual(address.customer.first_name, 'zeinab')
        self.assertEqual(address.province, 'Tehran')
        self.assertEqual(address.city, 'Tehran')
        self.assertEqual(address.complete_address, 'Tehran, Tehran, khoone')
        self.assertEqual(address.is_active, True)
        self.assertEqual(address.is_deleted, False)