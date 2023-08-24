from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('forgot-password/verify/<uidb64>/<token>/', views.forgot_password_verify, name='forgot-password-verify'),
    path('reset-password/', views.reset_password, name='reset-password'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/edit-profile', views.edit_profile, name='edit-profile'),
    path('profile/change-password', views.change_password, name='change-password'),

    path('address/', views.address, name='user-address'),
    path('address/add-new-address', views.add_new_address, name='add-new-address'),
    path('address/delete-address/<int:address_id>/', views.delete_address, name='delete-address'),
    path('address/edit-address/<int:address_id>/', views.edit_address, name='edit-address'),


    path('orders/', views.orders, name='user-orders'),
    path('orders/<str:order_id>/', views.order_details, name='user-order-details'),
    path('orders/cancel-order/<int:id>/', views.cancel_order, name='user-order-cancel'),
    path('orders/return-order/<int:id>/', views.return_order, name='user-order-return'),

    
]