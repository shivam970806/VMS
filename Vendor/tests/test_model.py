from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from ..models import *


class UserModelTest(TestCase):
    def test_create_user(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))


    def test_create_superuser(self):
        username = "shivamsharma"
        password = "shivam1234"
        email = "shivamsharma@gmail.com"
        first_name = "shivam"
        last_name = "sharma"

        superuser = User.objects.create_superuser(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        self.assertEqual(superuser.username, username)
        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.first_name, first_name)
        self.assertEqual(superuser.last_name, last_name)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password(password))



class VendorModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shivamsharma', password='shivam@1234')

    def test_vendor_creation(self):
        vendor = Vendor.objects.create(
            name='Microsoft',
            contact_details=90134345,
            address="Cleveland, USA",
            vendor_code="MI68",
            created_by=self.user
        )

        self.assertEqual(vendor.name, 'Microsoft')
        self.assertEqual(vendor.contact_details, 90134345)
        self.assertEqual(vendor.address, "Cleveland, USA")
        self.assertEqual(vendor.vendor_code, "MI68")
        self.assertIsNotNone(vendor.created_at)
        self.assertIsNotNone(vendor.updated_at)
        self.assertEqual(vendor.created_by, self.user)

    def test_vendor_str_method(self):
        vendor = Vendor.objects.create(
            name='Microsoft',
            contact_details=90134345,
            address="Cleveland, USA",
            vendor_code="MI68",
            created_by=self.user
        )
        self.assertEqual(str(vendor), 'Microsoft')


class PurchaseOrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shivamsharma', password='shivam@1234')
        self.vendor = Vendor.objects.create(
            name='Microsoft',
            contact_details=90134345,
            address="Cleveland, USA",
            vendor_code="MI68",
            created_by=self.user
        )

    def test_purchase_order_creation(self):
        purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            delivery_date=datetime.now() + timedelta(days=7),
            items={'Notebook': 10},
            quantity=444,
            created_by=self.user
        )
        self.assertIsNotNone(purchase_order.po_number)
        self.assertEqual(purchase_order.vendor, self.vendor)
        self.assertIsNotNone(purchase_order.order_date)
        self.assertIsNotNone(purchase_order.delivery_date)
        self.assertEqual(purchase_order.items, {'Notebook': 10})
        self.assertEqual(purchase_order.quantity, 444)
        self.assertEqual(purchase_order.status, 'Pending')
        self.assertEqual(purchase_order.created_by, self.user)
        self.assertFalse(purchase_order.on_time_delivery)
        self.assertEqual(str(purchase_order), purchase_order.po_number)

    # def test_purchase_order_save_method(self):
    #     purchase_order = PurchaseOrder.objects.create(
    #         vendor=self.vendor,
    #         delivery_date=datetime.now() + timedelta(days=7),
    #         items={'Notebook': 10},
    #         quantity=444,
    #         status='Pending',
    #         created_by=self.user
    #     )
    #     self.assertIsNotNone(purchase_order.response_time)


class HistorialPerformanceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shivamsharma', password='shivam@1234')
        self.vendor = Vendor.objects.create(
            name='Microsoft',
            contact_details=90134345,
            address="Cleveland, USA",
            vendor_code="MI68",
            created_by=self.user
        )

    def test_historical_performance_creation(self):
        historical_performance = HistorialPerformance.objects.create(
            vendor=self.vendor,
            on_time_delivery_rate=95.5,
            quality_rating_avg=8.7,
            average_response_time=24.5,
            fulfillment_rate=98.2,
            created_by=self.user
        )
        self.assertEqual(historical_performance.vendor, self.vendor)
        self.assertEqual(historical_performance.on_time_delivery_rate, 95.5)
        self.assertEqual(historical_performance.quality_rating_avg, 8.7)
        self.assertEqual(historical_performance.average_response_time, 24.5)
        self.assertEqual(historical_performance.fulfillment_rate, 98.2)
        self.assertEqual(historical_performance.created_by, self.user)
        self.assertEqual(str(historical_performance), self.vendor.name)
