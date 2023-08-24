from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.products, name='products'),
    path('view/<slug:product_slug>/', views.product_view, name='product-view'),
    path('search/', views.search, name='search')
    
]