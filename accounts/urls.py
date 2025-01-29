from django.urls import path, include
from . import views

urlpatterns = [
    
    path('register/',views.register,name="registration"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('changePassword/', views.changePassword, name="changePassword"),
    path('myOrders/', views.my_orders, name="myOrders"),
    path('activate/<uidb64>/<token>', views.activate, name = "activate"),
    path('order_detail/<int:order_number>',views.order_detail,name="order_detail"),
    
   
   
] 