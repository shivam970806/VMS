from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('signup', views.Signup.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('vendors', views.VendorAPI.as_view(), name='Vendors'),
    path('vendors/<str:id>', views.VendorDataAPI.as_view(), name='VendorsData'),
    path('vendors/<str:id>/performance', views.PerformanceAPI.as_view(), name='VendorsPerformance'),
    path('purchase_orders', views.PurchaseOrderAPI.as_view(), name='PurchaseOrders'),
    path('purchase_orders/<str:id>', views.PurchaseOrderDataAPI.as_view(), name='PurchaseOrdersData'),
    path('purchase_orders/<str:id>/acknowledge', views.OrderAcknowledge.as_view(), name='PurchaseOrderAcknowledged'),
]
