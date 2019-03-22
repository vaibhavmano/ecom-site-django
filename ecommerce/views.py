from django.shortcuts import render, get_object_or_404, render_to_response
from django.core import serializers #Convert to JSON
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User #Default User model
from .models import CustomUser, CustomSeller, ProductsInfo, CartInfo, OrderInfo, SellerOrderInfo, WishlistInfo
from .serializers import CustomSerializer,ContactSerializer, SellerSerializer,ProductSerializer, CartSerializer,OrderSerializer, SellerOrderSerializer, WishSerializer, UserSerializer #From serializers.py
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
from django.db.models import Q
import random #Random number generator
import uuid
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.http import require_GET


from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

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
def productsfilter(request, filter_id):
    if filter_id is "W":
        disp = ProductsInfo.objects.filter(gender = 'Female')
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
        # return HttpResponse("Women")
    elif filter_id is "M":
        disp = ProductsInfo.objects.filter(gender = 'Male')
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
    elif filter_id is 1:
        disp = ProductsInfo.objects.filter(Q(colors__icontains='blue'))
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
    elif filter_id is 2:
        disp = ProductsInfo.objects.filter(Q(colors__icontains='red'))
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
    elif filter_id is 3:
        disp = ProductsInfo.objects.filter(Q(colors__icontains='black'))
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
    elif filter_id is 5:
        disp = ProductsInfo.objects.filter(price__gte=0, price__lte=50)
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
    elif filter_id is 100:
        disp = ProductsInfo.objects.filter(price__gte=100, price__lte=200)
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})
    elif filter_id is 250:
        disp = ProductsInfo.objects.filter(price__gte=250)
        paginator = Paginator(disp, 9)
        page = request.GET.get('page')
        disp = paginator.get_page(page)
        return render(request, 'product.html', {'products': disp})


#Customer
def cart(request):
    cartdisp = CartInfo.objects.all()
    return render(request, 'cart.html', {'cart': cartdisp})

#Customer
def verifyTemp(request):
    return render(request, 'verifymail.html')

#Customer
def orders(request):
    return render(request, 'orders.html')

#Customer
def wishlist(request):
    return render(request, 'wishlist.html')

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
    # orderObj = CartInfo.objects.all().values('nameofprod')
    global orderinvoice
    amount = OrderInfo.objects.filter(orderInvoiceNum = orderinvoice).values("totalprice")
    paypal_dict = {
        "business": "youremail@gmail.com",
        "amount": amount[0]['totalprice'],
        "item_name": "ECOMMERCE",
        "invoice": orderinvoice,
        "currency_code": 'INR',
        "hosted_button_id": 'TPAEKT6HW6B4Q',
        "notify_url": "https://fb6c4cdd.ngrok.io/notify-ppal",
        "return": "https://fb6c4cdd.ngrok.io/complete-payment",  #complete-payment",
        "cancel_return": "https://fb6c4cdd.ngrok.io/cancel-payment",
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    paypalform = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": paypalform}
    return render(request, "payment.html", context)



# -------------
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    global orderinvoice
    # if ipn_obj.payment_status == ST_PP_COMPLETED:
        
    if ipn_obj.receiver_email != "youremail@gmail.com":
            orderObj = get_object_or_404(OrderInfo, orderInvoiceNum = orderinvoice)
            orderObj.paymentstatus = "DECLINED"
            orderObj.save()
            print("Declined")
            # return
        
    else:
        # if ipn_obj.payment_status == 'Completed':            
        orderObj = get_object_or_404(OrderInfo, orderInvoiceNum = orderinvoice)
        orderObj.paymentstatus = "ACCEPTED"
        orderObj.save()
            # print("Accepted")
        print("Accepted")
        

valid_ipn_received.connect(show_me_the_money)

# -------------


@csrf_exempt
def payment_complete(request):
    args = {'POST': request.POST, 'GET': request.GET}
    return render_to_response('complete-payment.html', args)


@csrf_exempt
def payment_cancel(request):
    args = {'POST': request.POST, 'GET': request.GET}
    return render_to_response('cancel-payment.html', args)


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
    global usernameCustomer
    global sixRandom
    sixRandom = random.randint(111111,999999)
    # global verifyUUID
    # verifyUUID = str(uuid.uuid4())
    usernameCustomer = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("firstname")
    phonenum = request.data.get("phonenum")
    data = {
        'user': 
            {
                'username': usernameCustomer,
                'password': password,
                'email': usernameCustomer,
            },
        'first_name': name,
        'phone_number': phonenum,
    }
    #Fetch - Over
    serializer = CustomSerializer(data = data)
    if serializer.is_valid():
        serializer.create(validated_data = data)
        # Send random number
        subject = 'Verify your email address'
        # mailmessage = "Click on this link to verify email address " + "http://127.0.0.1:8000/activate/"+ verifyUUID +"/"+ usernameCustomer  #use this to verify using email
        mailmessage = "Your verification code is '" + str(sixRandom) + "'"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [usernameCustomer,]
        send_mail( subject, mailmessage, email_from, recipient_list ) 
        
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
        global orderinvoice
        orderinvoice = random.randint(111111,999999)
        data = {
            'totalprice': totalprice,
            'products': cartData,
            'customer': userObj,
            'orderInvoiceNum': orderinvoice,
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



#Add to Wishlist for respective user
#api-wishinsert
@csrf_exempt
@api_view(["POST"])
def wishinsert(request):
    user = request.user
    userObj = findUser(user)
    if not userObj:
        return HttpResponse("Not Found")
    else:
        cartData = request.data.get("nameofprod")
        userObj = userObj[0]['id']
        data = {
            'products': cartData,
            'customer': userObj
        }
        serializer = WishSerializer(data = data)
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
def wishlistdisp(request):
    user = request.user
    userObj = findUser(user)
    r = userObj[0]['id']
    if not userObj:
        return Response("Not valid")
    else:
        wishdisp = WishlistInfo.objects.filter(customer = r)
        data = serializers.serialize('json', wishdisp)
        return HttpResponse(data)


@csrf_exempt
@api_view(["POST"])
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

#Products Delete
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


#Wishlist Delete
@csrf_exempt
@api_view(["POST"])
def wishlistdelete(request):
    user = request.user
    userObj = findUser(user)
    r = userObj[0]['id']
    if not userObj:
        return Response("Not a Customer", status = HTTP_404_NOT_FOUND)
    else:
        prodname = request.data.get("prodname")
        messagee = WishlistInfo.objects.filter(products = prodname, customer_id = r).delete()
        return Response(messagee)


# Two step verification using email
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def verifyemail(request):
    global sixRandom
    global usernameCustomer
    randomNum = request.data.get('randomNum')
    randomNum = int(randomNum)
    # typeofNym = type(randomNum)
    if( randomNum == sixRandom):
        userObj = get_object_or_404(User, username = usernameCustomer)
        userObj.is_active = True
        userObj.save()
        return Response("Verified", status=HTTP_200_OK)

    else:
        return HttpResponse('Not Verified')

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def delemail(request):
    global usernameCustomer
    User.objects.filter(username = usernameCustomer).delete()
    return Response("Deleted", status=HTTP_200_OK)


# Activate using link
# def activatemail(request):
#     global usernameCustomer
#     global verifyUUID
#     newlink = request.get_full_path()
#     getUUID = newlink.split('/').pop(2)
#     getUser = newlink.split('/').pop(3) 
#     if getUUID == verifyUUID:
#         if usernameCustomer == getUser:
#             userObj = get_object_or_404(User, username = usernameCustomer)
#             userObj.is_active = True
#             userObj.save()
#             return render(request, 'verifycomplete.html')
#     else:
#         User.objects.filter(username = usernameCustomer).delete()
#         return HttpResponse("Error", status=HTTP_400_BAD_REQUEST)


# Testing
# @csrf_exempt
# @api_view(["GET"])
# @permission_classes((AllowAny,))
# def datatest(request):
#     hi = request.data.get("FilterVar")
#     hello = "Hello " + str(hi)
#     return HttpResponse(hello)

