from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, str) -> str:
        """ A function to save the password for storing the values """
        return make_password(str)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['username', 'password']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['id', 'created_at', 'updated_at']
        read_only_fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        extra_kwargs = {'created_by': {'write_only': True}}
        

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        read_only_fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['po_number', 'order_date', 'issue_date', 'acknowledgment_date', 'response_time', 'on_time_delivery']
        extra_kwargs = {'created_by': {'write_only': True}, 'vendor':{'write_only': True}}
