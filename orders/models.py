from django.db import models
from accounts.models import Account, Address
from product.models import Products

# Create your models here.
class Payment(models.Model):

    status=(
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Failed','Failed'),
        ('Successful','Successful'),
        ('Refunded','Refunded'),
    )

    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, null=False)
    status=models.CharField(max_length=100, choices=status,default='Pending')
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

status=(
    ('Pending','Pending'),
    ('Placed','Placed'),
    ('Processing','Processing'),
    ('Shipped','Shipped'),
    ('Out for Delivery','Out for Delivery'),
    ('Delivered','Delivered'),
    ('Returned','Returned'),
    ('Return Confirmed','Return Confirmed'),
    ('Cancelled','Cancelled'),
)

class Order(models.Model):
    
    
    # razor_pay_order_id = models.CharField(max_length=100, null=True, blank = True)
    # razor_pay_payment_id = models.CharField(max_length=100, null=True, blank = True)
    # razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank = True)
    user=models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    payment=models.ForeignKey(Payment, on_delete=models.DO_NOTHING, blank=True, null=True)
    order_id=models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    gross_amount = models.PositiveIntegerField()
    shipping_charge = models.PositiveIntegerField()
    order_total=models.FloatField()
    order_tax= models.FloatField()
    status=models.CharField(max_length=20,choices=status,default='Pending')
    ip=models.CharField(max_length=20,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.order_id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20,choices=status)
    note = models.TextField(max_length = 500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.order_id)

class OrderProduct(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price = models.PositiveIntegerField()
    total= models.PositiveIntegerField()
    gross_amount = models.PositiveIntegerField()
    is_ordered=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def total_amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

