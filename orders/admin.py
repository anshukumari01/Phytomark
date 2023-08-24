from django.contrib import admin
from .models import *

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model= OrderProduct
    list_display=['order','product','price','quantity']
    readonly_fields=('payment','user','product','quantity','order')
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','user','order_total','order_tax', 'status','is_ordered','created_date']
    list_filter=['status','is_ordered']
    search_fields=['order_id']
    list_per_page=20
    inlines=[OrderProductInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display=['payment_id','user','amount','status','created_date']
    list_filter=['status']
    search_fields=['payment_id']
    list_per_page=20

class OrderProductAdmin(admin.ModelAdmin):
    list_display=['order','product','price','quantity']
    list_per_page=20

class OrderDetailsAdmin(admin.ModelAdmin):
  list_display=['order','order_status','date']

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
