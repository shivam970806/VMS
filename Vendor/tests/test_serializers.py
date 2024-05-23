from ..serializers import *
from ..models import *
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta


class UserSerializerTestCase(TestCase):
    def test_user_serializer_valid_data(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"
        data = {
            'username':username,
            'password': password,
            'email':email,
            'first_name': first_name,
            'last_name': last_name
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_user_serializer_duplicate_username(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"
        User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        data = {
            'username':username,
            'password': "shivam",
            'email':"shivamsharma123@gmail.com",
            'first_name': "shivam",
            'last_name': "sharma"
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['username'][0], 'A user with that username already exists.')

    def test_user_serializer_create(self):
        data = {
            'username':"shivamsharma",
            'password': "shivam",
            'email':"shivamsharma123@gmail.com",
            'first_name': "shivam",
            'last_name': "sharma"
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.create(serializer.validated_data)
        self.assertEqual(user.username, "shivamsharma")
        self.assertEqual(user.email, "shivamsharma123@gmail.com")
        self.assertEqual(user.first_name, "shivam")
        self.assertEqual(user.last_name, "sharma")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("shivam"))

    def test_user_serializer_update(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        data = {
            'first_name': 'shivam',
            'last_name':'Patil'
        }

        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.update(user, serializer.validated_data)
        self.assertEqual(updated_user.first_name, 'shivam')
        self.assertEqual(updated_user.last_name, 'Patil')


class LoginSerializerTests(TestCase):
    def setUp(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"
        self.user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

    def test_login_serializer_valid_data(self):
        data = {'username': "shivamsharma", 'password': "shivam1234"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], "shivamsharma")

    def test_login_serializer_invalid_data(self):
        data = {'name': "shivamsharma", 'password': "sharma123"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('This field is required.', serializer.errors['username'])


class VendorSerializerTests(TestCase):
    def setUp(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"
        self.user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

    def test_vendor_serializer(self):
        data = {
            'name': 'Microsoft',
            'contact_details': 9013434545,
            'address': "Cleveland, USA",
            'vendor_code': "MI68",
            'created_by': self.user.id
        }

        serializer = VendorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vendor = serializer.save()
        self.assertEqual(vendor.name, 'Microsoft')
        self.assertEqual(vendor.contact_details, 9013434545)
        self.assertEqual(vendor.address, "Cleveland, USA")
        self.assertEqual(vendor.vendor_code, "MI68")


class PerformanceSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shivamsharma', password='shivam@1234')
        self.vendor = Vendor.objects.create(
            name='Microsoft',
            contact_details=90134345,
            address="Cleveland, USA",
            vendor_code="MI68",
            created_by=self.user
        )

    def test_performance_serializer(self):
        data = {'vendor': self.vendor.id}
        serializer = PerformanceSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class PurchaseOrderSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shivamsharma', password='shivam@1234')
        self.vendor = Vendor.objects.create(
            name='Microsoft',
            contact_details=90134345,
            address="Cleveland, USA",
            vendor_code="MI68",
            created_by=self.user
        )

    def test_purchase_order_serializer(self):
        data = {
            "vendor": self.vendor.id,
            'delivery_date': datetime.now() + timedelta(days=7),
            'items': {'Laptop': 5},
            'quantity': 10,
            'created_by': self.user.id
        }

        serializer = PurchaseOrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        purchase_order = serializer.save()
        self.assertIsNotNone(purchase_order.po_number)
        self.assertEqual(purchase_order.vendor, self.vendor)
        self.assertEqual(purchase_order.status, 'Pending')
        self.assertEqual(purchase_order.created_by, self.user)
