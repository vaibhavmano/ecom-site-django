from rest_framework import serializers
from django.contrib.auth.models import User #Default User model
from .models import CustomUser, ContactInfo, CustomSeller, ProductsInfo, CartInfo, OrderInfo, SellerOrderInfo
from rest_framework.response import Response




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username','email', 'password') #use username instead of email if error
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

#User/Customer
class CustomSerializer(serializers.ModelSerializer):

    user = UserSerializer(required = True)  #Serialize user

    class Meta:
        model = CustomUser
        fields = ('user','first_name', 'phone_number')

    def create(self, validated_data):
        user_data = validated_data.pop('user') #Pop user into user_data
        user = UserSerializer.create(UserSerializer(), user_data) #create by calling serializer
        custom= CustomUser.objects.update_or_create(user = user, first_name = validated_data.pop('first_name'), phone_number = validated_data.pop('phone_number')) #Create custom serializer 
        return custom


# Seller/Merchant
class SellerSerializer(serializers.ModelSerializer):

    user = UserSerializer(required = True)  #Serialize user

    class Meta:
        model = CustomSeller
        fields = ('user','company_name', 'phone_number', 'company_address')

    def create(self, validated_data):
        user_data = validated_data.pop('user') #Pop user into user_data
        user = UserSerializer.create(UserSerializer(), user_data) #create by calling serializer
        custom= CustomSeller.objects.update_or_create(user = user, company_name = validated_data.pop('company_name'), phone_number = validated_data.pop('phone_number'), company_address = validated_data.pop('company_address') ) #Create custom serializer 
        return custom


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInfo
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartInfo
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'

class SellerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerOrderInfo
        fields = '__all__'