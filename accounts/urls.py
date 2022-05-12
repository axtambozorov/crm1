from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name='main'),
    path('customers/<str:pk_test>/',customers, name='customers'),
    path('users',userspage,name='users'),
    path('profile/',profilepage,name='profile'),
    path('editprofile/',edit_profile,name='editprofile'),

    path('products/',products, name='products'),
    path('create_product/',createproduct, name='create_product'),

    path('create_customer/',createcustomer, name='create_customer'),
    path('updatecustomer/<str:pk>/',updatecustomer, name='updatecustomer'),
    path('deletecustomer/<str:pk>/',deletecustomer, name='deletecustomer'),

    path('create_order/',createorder, name='create_order'),
    path('updateorder/<str:pk>/',updateorder, name='updateorder'),
    path('deleteorder/<str:pk>/',deleteorder, name='deleteorder'),

    path('create_orders_customer/<str:pk>/',createorderscustomer, name='createorderscustomer'),


    path('login/',loginpage,name='login'),
    path('register/',register,name='register'),
    path('logout/',logoutpage,name='logout'),



]