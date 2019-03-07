from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products, name='products'),
    path('cart/',views.cart, name='cart'),
    path('blog/',views.blog, name='blog'),
    path('about/',views.about, name='about'),
    path('contact/',views.contactTemp, name='contact'),
    path('api/contact/',views.contact, name='api-contact'), #Receive data from contact forms
    path('api/login', views.login, name='auth-login'), #Token generation
    path('login/', views.loginTemp, name='login'), #login form
    path('seller/', views.sellerLoginTemp, name='seller-login'), #Seller login
    path('seller/signup', views.sellerSignupTemp, name='seller-signup'),
    path('signup/', views.signupTemp, name='signup'), #Signup form
    path('api/sampleapi', views.sample_api, name='api-view-data'), #viewing data
    path('api/signup', views.signup, name='api-signup'), #Customer SignUp
    path('orders/', views.orders, name='orders'), #Order display
    path('api/sellersignup', views.signupseller, name='api-sellersignup'), #Seller SignUp
    path('seller/productreg/', views.productRegTemp, name='productreg'), #Product registration Template
    path('api/productreg', views.productreg, name='api-productreg'), #Product detail insertion
    # path('api/productdisp', views.productdisp, name='api-productdisp'), #Product display
    path('api/cartinsert', views.cartinsert, name='api-cartinsert'), #Cart display
    path('cartempty/', views.cartempty, name='empty-cart'), #Empty cart
    path('payment/', views.paymentTemp, name='payment'), #Payment page display
    path('api/orderinsert', views.orderinsert, name='api-orderinsert'), #Insert order with respect to user token
    path('api/orders', views.orderdisp, name='order-disp'), #Order display
    path('seller/orders', views.sellerorderTemp, name='seller-order'), #Order display Template for SELLER
    path('seller/api/orders', views.sellerorderdisp, name='seller-order-disp'), #Order display for SELLER
    path('seller/products', views.sellerproductTemp, name='seller-product'), #Product display Template for SELLER
    path('seller/api/products', views.sellerproductdisp, name='seller-product-disp'), #Order display for SELLER
    path('seller/api/productsedit', views.productedit, name='seller-product-edit'), #Order edit for SELLER
    path('seller/api/productsdelete', views.productdelete, name='seller-product-delete'), #Order edit for SELLER
    path('api/delete', views.cartdelete, name='delete-cart'), #Delete item from cart

    # Test Path ----- Use this path to test for data insertion and retrieval
    # path('api/datatest', views.datatest, name='testing'), #Testing-------

    # path('api-token-auth/', obtain_auth_token, name='api-token-auth'), #Testing default token assign

]