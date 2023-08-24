from django.db import models
from accounts.models import Account
from product.models import Products

# Create your models here.
class Cart(models.Model):
  cart_id = models.CharField(max_length=255, blank=True)
  date_created = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.cart_id
  
class CartItem(models.Model):
  user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)

  def sub_total(self):
    return self.product.price * self.quantity

  def __str__(self):
    return self.product.name
  
 

class ShippingCharge(models.Model):
    range_upto = models.PositiveIntegerField()
    shipping_charge = models.PositiveIntegerField()


class Tax(models.Model):
  tax_percentage = models.DecimalField(decimal_places=2, max_digits=10)
