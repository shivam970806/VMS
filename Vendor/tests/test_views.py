from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import *

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup(self):
        url = '/api/signup'

        # Positive Testing
        data = {'username': 'shivamsharma', 'password': 'shivam1234', 'first_name': "shivam", 'last_name': "sharma",
                'email': 'shivamsharma12@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'User Created Successfully')
        self.assertEqual(response.data['data']['username'], 'shivamsharma')
        self.assertEqual(response.data['data']['first_name'], 'shivam')
        self.assertEqual(response.data['data']['last_name'], 'sharma')
        self.assertEqual(response.data['data']['email'], 'shivamsharma12@gmail.com')

        # Negative testing with Incomplete Data
        incomplete_data = {'username': 'shivamsharma', 'password': 'shivam1234'}
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertIn('Missing required fields', response.data['message'])


    def test_login(self):
        url = '/api/login'
        user = User.objects.create_user(username='shivamsharma', password='shivam1234')
        user.is_active = False
        user.save()

        data = {'username': 'shivamsharma', 'password': 'shivam1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'User Successfully Logged')
        self.assertIn('access', response.data['data'])
        
        invalid_data = {'username': 'shivampatil', 'password': 'shivam333'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['status'])
        self.assertIn('Invalid Login Credential', response.data['message'])

        Wrong_data = {'username1': 'shivamsharma', 'secrete': 'shivam333'}
        response = self.client.post(url, Wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['status'])
        self.assertIn('Invalid Login Credential', response.data['message'])

class VendorAPITests(TestCase):
    fixtures = ['Vendor/tests/main.json']
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='shivamsharma', password='shivam1234')
        self.client.force_authenticate(user=self.user)

    def test_vendor(self):
        # url_login = '/api/login'
        # user = User.objects.create_user(username='shivamsharma', password='shivam1234')
        # login_data = {'username': 'shivamsharma', 'password': 'shivam1234'}
        # login_response = self.client.post(url_login, login_data, format='json')
        # bearer_token = login_response.data['data']['access']
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {bearer_token}')

        # Create Vender
        url_vendor = '/api/vendors'

        # Positive Testing
        vendor_data = { "name": "Apple",
                        "contact_details": 9834557675,
                        "address": "New York, USA",
                        "vendor_code": "AP66",
                    }
        response = self.client.post(url_vendor, vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Vendor Created Successfully')

        # Negative Testing - Same Vendor
        vendor_data = { "name": "Microsoft",
                        "contact_details": 90134345,
                        "address": "Cleveland, USA",
                        "vendor_code": "MI68",
                    }
        response = self.client.post(url_vendor, vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertEqual(response.data['message'], 'Incorrect Detail')

        # Negative Testing - Missing required field(name)
        invalid_vendor_data = {"contact_details": 90134345, "address": "Cleveland, USA", "vendor_code": "MI68"}
        response = self.client.post(url_vendor, invalid_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertIn("Incorrect Detail", response.data['message'])

    def test_get_all_vendors(self):
        url_vendor = '/api/vendors'
        response = self.client.get(url_vendor, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data')
        self.assertGreater(len(response.data['data']), 0)

    def test_get_vendor_by_id(self):
        # url_login = '/api/login'
        # login_data = {'username': 'shivamsharma', 'password': 'shivam1234'}
        # login_response = self.client.post(url_login, login_data, format='json')
        # bearer_token = login_response.data['data']['access']
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {bearer_token}')
        # # url_vendor = '/api/vendors'
        # # response = self.client.get(url_vendor, format="json")
        vendor = Vendor.objects.create(name="Mahindra", contact_details=9876423457, address="Mumbai, India", vendor_code="MAHI07", created_by=self.user)
        # url_vendor = '/api/vendors'

        # # # Positive Testing
        # vendor_data = { "name": "Apple",
        #                 "contact_details": 9834557675,
        #                 "address": "New York, USA",
        #                 "vendor_code": "AP66",
        #             }
        # self.client.post(url_vendor, vendor_data, format='json')
        url = f'/api/vendors/MAHI07'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data')
        self.assertEqual(response.data['data']['name'], 'Mahindra')
        self.assertEqual(response.data['data']['contact_details'], 9876423457)
        self.assertEqual(response.data['data']['address'], 'Mumbai, India')
        self.assertEqual(response.data['data']['vendor_code'], 'MAHI07')
        self.assertEqual(response.data['data']['on_time_delivery_rate'], None)
        self.assertEqual(response.data['data']['quality_rating_avg'], None)
        self.assertEqual(response.data['data']['average_response_time'], None)
        self.assertEqual(response.data['data']['fulfillment_rate'], None)


        # Negative Test Cases
        url = '/api/vendors/DD35'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['status'])
        self.assertIn('Something went wrong', response.data['message'])

    def test_update_vendor(self):
        vendor = Vendor.objects.create(name="Mahindra", contact_details=9876423457,
                                       address="Mumbai, India", vendor_code="MAHI07", created_by=self.user)
        url = f'/api/vendors/{vendor.vendor_code}'

        updated_data = {"name": "TCS", "contact_details": 7890125555, "address": "Navi Mumbai"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data updated')
        self.assertEqual(response.data['data']['name'], "TCS")
        self.assertEqual(response.data['data']['contact_details'], 7890125555)
        self.assertEqual(response.data['data']['address'], "Navi Mumbai")

        invalid_data = {"name": ""}
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertIn('Something went wrong', response.data['message'])

        invalid_data = {}
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(response.data['status'])
        self.assertIn("Data not Found", response.data['message'])

    def test_delete_vendor(self):
        vendor = Vendor.objects.create(name="Mahindra", contact_details=9876423457,
                                       address="Mumbai, India", vendor_code="MAHI07", created_by=self.user)
        url = f'/api/vendors/{vendor.vendor_code}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Deleted')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['status'])
        self.assertIn('Something went wrong', response.data['message'])
    

class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='shivamsharma', password='shivam1234')
        self.client.force_authenticate(user=self.user)
        self.vendor = Vendor.objects.create(name="Mahindra", contact_details=9876423457, address="Mumbai, India", vendor_code="MAHI07", created_by=self.user)

    def test_create_purchase_order(self):
        url = '/api/purchase_orders'

        # Positive Testing
        data = {
                    "vendor_name": "Mahindra",
                    "items": {
                        "Pen": 6
                    },
                    "quantity": 7,
                    "delivery_date": "2024-04-02T17:43:59"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Purchase Order Created Successfully')

        # Negative Testing - Missing Vendor Name
        invalid_data = {'quantity': 10, 'total_amount': 100.50, 'created_by': self.user.id}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['status'])
        self.assertIn('Vendor name is required', response.data['message'])

        # Negative Testing - Adding Quality Rating and Status in Creation
        invalid_data = {"vendor_name": "Mahindra", 'quantity': 10, 'total_amount': 100.50, 'quality_rating': 8, 'status': 'Pending', 'created_by': self.user.id}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertIn('Cannot add quality rating and status in creation', response.data['message'])

    def test_get_all_purchase_orders(self):
        url = '/api/purchase_orders'
        data = {
                    "vendor_name": "Mahindra",
                    "items": {
                        "Pen": 6
                    },
                    "quantity": 7,
                    "delivery_date": "2024-04-02T17:43:59"
                }
        self.client.post(url, data, format='json')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data')
        self.assertGreater(len(response.data['data']), 0)

        url = f'/api/vendors/{self.vendor.vendor_code}/performance'
        # Positive Testing
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data')
        performance_metrics = response.data['data']
        self.assertIn('average_response_time', performance_metrics)
        self.assertIn('on_time_delivery_rate', performance_metrics)
        self.assertIn('quality_rating_avg', performance_metrics)
        self.assertIn('fulfillment_rate', performance_metrics)

        url = '/api/vendors/LL34/performance'
        # Negative Testing - Nonexistent Vendor
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['status'])
        self.assertIn('Something went wrong', response.data['message'])

class PurchaseOrderDataAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='shivamsharma', password='shivam1234')
        self.client.force_authenticate(user=self.user)
        self.vendor = Vendor.objects.create(name="Mahindra", contact_details=9876423457, address="Mumbai, India",
                                            vendor_code="MAHI07", created_by=self.user)
        self.purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, items={"Pen": 6}, quantity=5,
                                                           delivery_date="2024-04-02T17:43:59", created_by=self.user)

    def test_get_purchase_order_by_id(self):
        url = f'/api/purchase_orders/{self.purchase_order.po_number}'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data')
        self.assertEqual(response.data['data']['po_number'], self.purchase_order.po_number)
        self.assertEqual(response.data['data']['quantity'], 5)
        self.assertEqual(response.data['data']['items'], {"Pen": 6})
        self.assertEqual(response.data['data']['delivery_date'], "2024-04-02T17:43:59")

    def test_update_purchase_order(self):
        url = f'/api/purchase_orders/{self.purchase_order.po_number}'

        # Positive Testing
        # TODO: before acknowledgement
        updated_data = {
                        "delivery_date": "2024-04-02T17:43:59",
                        "items": {
                            "Notebook":10
                        },
                        "quantity": 444,
                        # "status": "Completed",
                        # "quality_rating": 7
                    }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Data updated')
        self.assertEqual(response.data['data']['po_number'], self.purchase_order.po_number)
        self.assertEqual(response.data['data']['quantity'], 444)
        self.assertEqual(response.data['data']['items'], {"Notebook": 10})
        self.assertEqual(response.data['data']['delivery_date'], "2024-04-02T17:43:59")
        updated_data = {
                        "delivery_date": "2024-04-02T17:43:59",
                        "items": {
                            "Notebook":10
                        },
                        "quantity": 444,
                        "status": "Completed",
                        "quality_rating": 7
                    }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertEqual(response.data['message'], 'Can not change Status and quality rating before acknowledgement')
        self.assertEqual(response.data['data'], None)

        # Acknowledgement API
        # Negative testing
        url = '/api/purchase_orders/LJDS34-43523454-3454/acknowledge'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['status'])
        self.assertIn('Something went wrong', response.data['message'])

        # Positive Testing
        url = f'/api/purchase_orders/{self.purchase_order.po_number}/acknowledge'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['message'], 'Purchase order acknowledged')

        # TODO: After Acknowledgement
        # Negative Testing - Purchase Order already acknowledged
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_208_ALREADY_REPORTED)
        self.assertFalse(response.data['status'])
        self.assertIn('Purchase order already acknowledged', response.data['message'])

        # Negative Testing - Quality Rating is not Integer
        url = f'/api/purchase_orders/{self.purchase_order.po_number}'
        invalid_data = {'quantity': 6, "status": "Completed", 'quality_rating': '7'}
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.data['status'])
        self.assertIn('Quality rating is not Integer', response.data['message'])

        # Negative Testing - Can't Modify Completed or Cancelled Purchase Order
        invalid_data = {
                        "status": "Completed",
                        "quality_rating": 7
                    }
        response = self.client.put(url, invalid_data, format='json')
        invalid_data = {
                        "delivery_date": "2024-04-02T17:43:59",
                        "items": {
                            "Notebook":10
                        },
                        "quantity": 444,
                        "status": "Pending",
                        "quality_rating": 7
                    }
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)
        self.assertFalse(response.data['status'])
        self.assertIn('Can not modify purchase order once completed or cancelled', response.data['message'])
