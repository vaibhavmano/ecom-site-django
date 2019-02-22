from django.shortcuts import render
from django.core import serializers #Convert to JSON
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User #Default User model
from .models import CustomUser, ContactInfo
from .serializers import CustomSerializer,ContactSerializer, UserSerializer #From serializers.py
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

# Create your views here.
def home(request):
    return render(request, 'index.html')

def products(request):
    return render(request, 'product.html')

def cart(request):
    return render(request, 'cart.html')

def blog(request):
    return render(request, 'blog.html')

def about(request):
    return render(request, 'about.html')

def contactTemp(request):
    return render(request, 'contact.html')
    
def loginTemp(request):
    return render(request, 'login.html')

def signupTemp(request):
    return render(request, 'signup.html')

#Token Issue
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

#View data using token
#name = api-view-data
@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    getMyToken = request.META['HTTP_AUTHORIZATION']
    typeToken = getMyToken.split(' ')[1]
    data = User.objects.filter(auth_token = typeToken)
    data = serializers.serialize('json', data)
    return HttpResponse(data, status=HTTP_200_OK)




#SignUp
#name = api-signup
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    #Fetch data
    username = request.data.get("username")
    password = request.data.get("password")
    is_seller = request.data.get("isSeller")
    data = {
        'user': 
            {
                'username': username,
                'password': password,
                'email': username,
            },
        'is_seller': is_seller,
    }
    #Fetch - Over
    serializer = CustomSerializer(data = data)
    if serializer.is_valid():
        serializer.create(validated_data = data) 
        return Response (serializer.data, status=HTTP_200_OK)
        
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#Contact Info
#name = api-contact
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def contact(request):
    # Data fetch
    fullname = request.data.get("fullname")
    phonenumber = request.data.get("phone_num")
    email = request.data.get("email")
    message = request.data.get("message")
    data = {
        'fullname': fullname,
        'email_address': email,
        'phone_number': phonenumber,
        'message': message,
    }
    # Call custom serializer
    serializer = ContactSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data, status=HTTP_200_OK)
        # return Response("Completed")
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # return Response("none")
    
    
