
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
  
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('', views.home_view, name='home'),
     path('us/', views.us, name='us'),
       path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
