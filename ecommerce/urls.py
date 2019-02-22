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
    path('signup/', views.signupTemp, name='signup'), #Signup form
    path('api/sampleapi', views.sample_api, name='api-view-data'), #viewing data
    path('api/signup', views.signup, name='api-signup'), #Testing SignUp
    # path('api-token-auth/', obtain_auth_token, name='api-token-auth'), #Testing default token assign

]