from django.test import TestCase
from ..models import User, Address
from django.utils import timezone
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='zeinab',
            user_type = 'costumer',
            email = 'zeinab@gmail.com',
            phone_number = '09032554304',
            first_name = 'zeinab',
            last_name = 'moghadamnia',
            date_of_birth = '2002-07-23',
            image = None,
            is_active = True,
            is_deleted = False,
        )
    def test_user_model(self):
        self.assertEqual(self.user.username, 'zeinab')
        self.assertEqual(self.user.user_type, 'costumer')
        self.assertEqual(self.user.email, 'zeinab@gmail.com')
        self.assertEqual(self.user.phone_number, '09032554304')
        self.assertEqual(self.user.first_name, 'zeinab')
        self.assertEqual(self.user.last_name, 'moghadamnia')
        self.assertEqual(self.user.date_of_birth, '2002-07-23')
        self.assertEqual(self.user.image, None)
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_deleted, False)
class AddressModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            customer = User.objects.create_user(
                username='zeinab',
                user_type = 'costumer',
                email = 'zeinab@gmail.com',
                phone_number = '09032554304',
                first_name = 'zeinab',
                last_name = 'moghadamnia',
                date_of_birth = '2002-07-23',
                image = None,
            ),
            province = 'Tehran',
            city = 'Tehran',
            complete_address = 'Tehran, Tehran, Heravi',
            is_active=True,
            is_deleted=False,
        )

    def test_address_model(self):
        self.assertEqual(self.address.customer.first_name, 'zeinab')
        self.assertEqual(self.address.province, 'Tehran')
        self.assertEqual(self.address.city, 'Tehran')
        self.assertEqual(self.address.complete_address, 'Tehran, Tehran, Heravi')
        self.assertEqual(self.address.is_active, True)
        self.assertEqual(self.address.is_deleted, False)