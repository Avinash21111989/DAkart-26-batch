from django.urls import path, include
from . import views

urlpatterns = [
    
    path('add_cart/<int:product_id>',views.add_cart,name="addcart"),
    path('', views.cart,name='cart'),
    path('remove_cart_item/<int:product_id>', views.remove_cartItem, name = "RemovecartItem"),
    path('checkout/', views.checkout, name="checkout")
   
   
] 