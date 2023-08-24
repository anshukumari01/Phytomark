from django.urls import path
from . import views

urlpatterns = [
  path('address/save-address/', views.save_address , name='save-address'),
  path('payment-method/', views.payment_method , name='payment-method'),
  path('payment/', views.payment , name='payment'),
  path('order-success/', views.order_success , name='order-success'),
]