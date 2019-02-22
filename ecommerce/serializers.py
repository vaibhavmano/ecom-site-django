from rest_framework import serializers
from django.contrib.auth.models import User #Default User model
from .models import CustomUser, ContactInfo
from rest_framework.response import Response




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username','email', 'password') #use username instead of email if error
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class CustomSerializer(serializers.ModelSerializer):

    user = UserSerializer(required = True)  #Serialize user

    class Meta:
        model = CustomUser
        fields = ('user', 'is_seller',)

    def create(self, validated_data):
        user_data = validated_data.pop('user') #Pop user into user_data
        user = UserSerializer.create(UserSerializer(), user_data) #create by calling serializer
        custom= CustomUser.objects.update_or_create(user = user, is_seller = validated_data.pop('is_seller')) #Create custom serializer 
        return custom


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'

# class CustomSerializer(UserSerializer):

#     class Meta:
#         model = CustomUser
#         fields = ('username','password', 'is_seller')