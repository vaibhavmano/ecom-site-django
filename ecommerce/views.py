from django.shortcuts import render, get_object_or_404
from django.core import serializers #Convert to JSON
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User #Default User model
from .models import CustomUser, CustomSeller, ProductsInfo, CartInfo, OrderInfo, SellerOrderInfo
from .serializers import CustomSerializer,ContactSerializer, SellerSerializer,ProductSerializer, CartSerializer,OrderSerializer, SellerOrderSerializer, UserSerializer #From serializers.py
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

# Function to find user
def findUser(user):
    data = User.objects.filter(username = user).values('id')
    r = data[0]['id']
    userObj = CustomUser.objects.filter(user_id = r).values('id')
    return userObj



# Create your views here.
def home(request):
    return render(request, 'index.html')

#Customer
def products(request):
    disp = ProductsInfo.objects.all()
    paginator = Paginator(disp, 9)
    page = request.GET.get('page')
    disp = paginator.get_page(page)
    return render(request, 'product.html', {'products': disp})

#Customer
def cart(request):
    cartdisp = CartInfo.objects.all()
    return render(request, 'cart.html', {'cart': cartdisp})

#Customer
def orders(request):
    return render(request, 'orders.html')


#Customer
def blog(request):
    return render(request, 'blog.html')


#Customer    
def loginTemp(request):
    return render(request, 'login.html')

#Customer
def signupTemp(request):
    return render(request, 'signup.html')

#Customer
def paymentTemp(request):
    return render(request, 'payment.html')

#Seller
def sellerLoginTemp(request):
    return render(request, 'seller.html')

#Seller
def sellerSignupTemp(request):
    return render(request, 'sellersignup.html')


#Seller
def productRegTemp(request):
    return render(request, 'prodregistration.html')

#Seller
def sellerorderTemp(request):
    return render(request, 'sellerorder.html')

#Seller
def sellerproductTemp(request):
    return render(request, 'sellerproduct.html')



def cartempty(request):
    CartInfo.objects.all().delete()
    return HttpResponse("Deleted")


def about(request):
    return render(request, 'about.html')

def contactTemp(request):
    return render(request, 'contact.html')


#Testing SMS
# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def sendsms(request):
#     message = SmsMessage(body='lolcats make me hungry', from_phone='+41791111111', to=['+919487011501'])
#     message.send()

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
    # user = request.user #This works if you pass valid token! :D
    data = User.objects.filter(auth_token = typeToken).values('id')
    r = data[0]['id'] #Try using 'if' for classifying between seller and customer
    userObj = CustomUser.objects.filter(user_id = r).values('id')
    if not userObj:
        return HttpResponse(None)
    
    else:
        # data = serializers.serialize('json', userObj) #Comment this line while using 'r' variable in this view
        return HttpResponse(userObj, status=HTTP_200_OK)
    # return HttpResponse(user, status=HTTP_200_OK)

#SignUp
#Customer
#name = api-signup
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    #Fetch data
    username = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("firstname")
    phonenum = request.data.get("phonenum")
    data = {
        'user': 
            {
                'username': username,
                'password': password,
                'email': username,
            },
        'first_name': name,
        'phone_number': phonenum,
    }
    #Fetch - Over
    serializer = CustomSerializer(data = data)
    if serializer.is_valid():
        serializer.create(validated_data = data) 
        return Response (serializer.data, status=HTTP_200_OK)
        
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#SignUp
#Seller/Merchant
#name = api-sellersignup
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signupseller(request):
    #Fetch data
    companyuser = request.data.get("companyuser") #Email ID of company
    companyname = request.data.get("companyname")
    password = request.data.get("password")
    address = request.data.get("address")
    phonenum = request.data.get("phonenum")
    data = {
        'user': 
            {
                'username': companyuser,
                'password': password,
                'email': companyuser,
            },
        'company_name': companyname,
        'phone_number': phonenum,
        'company_address': address,       
    }
    #Fetch - Over
    serializer = SellerSerializer(data = data)
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
        subject = 'Thank you for contacting us!'
        mailmessage = " We'll get back to you shortly. This is the message you sent us '" + message + "'"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['vai.manohar@gmail.com',]
        send_mail( subject, mailmessage, email_from, recipient_list )
        return Response (serializer.data, status=HTTP_200_OK)
        
        # return Response("Completed")
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # return Response("none")



#Products Info
#name = api-productreg
@csrf_exempt
@api_view(["POST"])
def productreg(request):
    # Data fetch
    getMyToken = request.META['HTTP_AUTHORIZATION']
    typeToken = getMyToken.split(' ')[1]
    data = User.objects.filter(auth_token = typeToken).values('id')
    r = data[0]['id'] #get id of seller
    sellerobj = CustomSeller.objects.filter(user_id = r).values('id')
    if not sellerobj:
        return Response("Not a seller", status = HTTP_404_NOT_FOUND)
    else:
        nameofprod = request.data.get("prod_name")
        desc = request.data.get("prod_desc")
        size = request.data.get("size")
        gender = request.data.get("gender")
        colors = request.data.get("colors")
        category = request.data.get("category")
        price = request.data.get("price")
        data = {
            'nameofprod': nameofprod,
            'description': desc,
            'size': size,
            'gender': gender,
            'colors': colors,
            'category': category,
            'price':price,
            'seller': sellerobj[0]['id']
        }
    # Call serializer
        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=HTTP_200_OK)
            # return Response("Completed")
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            # return Response("none")


# Get products from database to display
# name = api-productdisp  
# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def productdisp(request):
#     disp = ProductsInfo.objects.all().values('nameofprod', 'price')
#     return Response(disp)
    
# Adding to cart
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def cartinsert(request):
    nameofprod = request.data.get("prod_name")
    price = request.data.get("price")
    seller_id = request.data.get("seller_id")
    data = {
        'nameofprod': nameofprod,
        'price': price,
        'seller': seller_id
    }
    # Call serializer
    serializer = CartSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data, status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

#Add to Order for respective user
#api-orderinsert
@csrf_exempt
@api_view(["POST"])
def orderinsert(request):
    user = request.user
    totalprice = request.data.get("totalprice")
    data = User.objects.filter(username = user).values('id')
    r = data[0]['id']
    userObj = CustomUser.objects.filter(user_id = r).values('id')
    cart = CartInfo.objects.all().values('nameofprod')    
    cartData = ""
    for i,c in enumerate(cart):
        cartData += str(i+1)+"."+c['nameofprod'] + ", "
    cartData = cartData[:-2] #Cart data in string
    if not userObj:
        return HttpResponse("Not Found")
    else:
        userObj = userObj[0]['id']
        data = {
            'totalprice': totalprice,
            'products': cartData,
            'customer': userObj
        }


        ###IMPORTANT
        # Getting seller (required) information from cart
        sellerinfo = CartInfo.objects.all().values('nameofprod','seller_id')
        for i in sellerinfo:
            sellerdata = {
                'products': i['nameofprod'],
                'seller': i['seller_id'],
                'customer': str(user)
            }
            serializerSeller = SellerOrderSerializer(data = sellerdata)
            if serializerSeller.is_valid():
                serializerSeller.save()
                # return Response (serializer.data, status=HTTP_200_OK)
            # else:
            #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        ###ENDS

        serializer = OrderSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def orderdisp(request):
    user = request.user
    userObj = findUser(user)
    r = userObj[0]['id']
    if not userObj:
        return Response("Not valid")
    else:
        orderdisp = OrderInfo.objects.filter(customer = r)
        data = serializers.serialize('json', orderdisp)
        return HttpResponse(data)

@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def sellerorderdisp(request):
    user = request.user
    data = User.objects.filter(username = user).values('id')
    r = data[0]['id']
    userObj = CustomSeller.objects.filter(user_id = r).values('id')
    r = userObj[0]['id']
    if not userObj:
        return Response("Not valid")
    else:
        sellerorderdisp = SellerOrderInfo.objects.filter(seller_id = r)
        data = serializers.serialize('json', sellerorderdisp)
        return HttpResponse(data)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def cartdelete(request):
    nameofprod = request.data.get("nameofprod")
    CartInfo.objects.filter(nameofprod = nameofprod).delete()
    return HttpResponse("completed")


@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def sellerproductdisp(request):
    user = request.user
    data = User.objects.filter(username = user).values('id')
    r = data[0]['id']
    userObj = CustomSeller.objects.filter(user_id = r).values('id')
    r = userObj[0]['id']
    if not userObj:
        return Response("Not valid")
    else:
        sellerproductdisp = ProductsInfo.objects.filter(seller_id = r)
        data = serializers.serialize('json', sellerproductdisp)
        return HttpResponse(data)


#Products Edit
@csrf_exempt
@api_view(["POST"])
def productedit(request):
    # Data fetch
    getMyToken = request.META['HTTP_AUTHORIZATION']
    typeToken = getMyToken.split(' ')[1]
    data = User.objects.filter(auth_token = typeToken).values('id')
    r = data[0]['id'] #get id of seller
    sellerobj = CustomSeller.objects.filter(user_id = r).values('id')
    if not sellerobj:
        return Response("Not a seller", status = HTTP_404_NOT_FOUND)
    else:
        prodid = request.data.get("prodid")
        desc = request.data.get("prodDesc")
        data = {
            'description': desc,
            'seller': sellerobj[0]['id']
        }
        prodObj = get_object_or_404(ProductsInfo, id = int(prodid))
    # Call serializer
        serializer = ProductSerializer(prodObj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=HTTP_200_OK)
            # return Response("Completed")
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            # return Response("none")

#Products Edit
@csrf_exempt
@api_view(["POST"])
def productdelete(request):
    getMyToken = request.META['HTTP_AUTHORIZATION']
    typeToken = getMyToken.split(' ')[1]
    data = User.objects.filter(auth_token = typeToken).values('id')
    r = data[0]['id'] #get id of seller
    sellerobj = CustomSeller.objects.filter(user_id = r).values('id')
    if not sellerobj:
        return Response("Not a seller", status = HTTP_404_NOT_FOUND)
    else:
        prodid = request.data.get("prodid")
        messagee = ProductsInfo.objects.filter(id = int(prodid), seller_id = r).delete()
        return Response(messagee)

# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def datatest(request):
#     user = request.user
#     hello = "Hello " + str(user)
#     return HttpResponse(hello)