from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Products
from home.models import About
from home.models import Info
from accounts.models import Address
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core.mail import send_mail
# Create your views here.


def _cart_id(request):
  cart_id = request.session.session_key
  if not cart_id:
    cart_id = request.session.create()
  return cart_id


def cart(request, total=0, tax=0, grand_total=0, shipping_cost = 0, quantity=0, cart_item=None):
    cart_items = CartItem.objects.none()
    try:
       if request.user.is_authenticated:
         cart_items = CartItem.objects.filter(user=request.user, is_active =True).order_by('-created_date')
        #  enquery = Enquery.objects.filter(user=request.user, is_confirmed = False).all()
       else:
         cart = Cart.objects.get(cart_id = _cart_id(request))
         cart_items = CartItem.objects.filter(cart=cart, is_active =True).order_by('-created_date')

       for cart_item in cart_items:
          total += cart_item.sub_total()
          quantity += cart_item.quantity

       shipping_charge = ShippingCharge.objects.first()
       if total <= shipping_charge.range_upto:
          shipping_cost = shipping_charge.shipping_charge
       
       tax_percent = Tax.objects.first().tax_percentage


       tax = (tax_percent*total)/100

       grand_total = total+tax+shipping_cost


       out_of_stock_item = None
       for cart_item in cart_items:
         if cart_item.quantity > cart_item.product.stock:
            out_of_stock_item = True
            break
         
    except ObjectDoesNotExist:
       out_of_stock_item = None
       pass
    
    about = About.objects.first()
    info = Info.objects.first()
    context={
        'about': about,
        'info': info,
       "total": total,
       "quantity" : quantity,
       "cart_items": cart_items,
       'out_of_stock_item':out_of_stock_item,
       'shipping_cost': shipping_cost,
       'tax' : tax,
       'grand_total' : grand_total,
      #  'enquery' : enquery,
    }

    return render(request, 'product/cart.html', context)

def add_to_cart(request, product_id):
    current_user = request.user
    product = Products.objects.get(id=product_id)
    if current_user.is_authenticated:
      try:
        cart_item = CartItem.objects.get(product=product, user=current_user)
        cart_item.quantity += 1
        cart_item.save()
      except CartItem.DoesNotExist:
       cart_item = CartItem.objects.create(
          product = product,
          quantity = 1,
          user = current_user,
       )
       cart_item.save()
      return redirect('cart')
    else:
        try:
          cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
          cart = Cart.objects.create(
            cart_id = _cart_id(request)
          )
        cart.save()

        try:
          cart_item = CartItem.objects.get(product=product, cart=cart)
          cart_item.quantity += 1
          cart_item.save()
        except CartItem.DoesNotExist:
          cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
          )
          cart_item.save()
        return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
  product = get_object_or_404(Products, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
      cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1 :
      cart_item.quantity -= 1
      cart_item.save()
    else:
       cart_item.delete()
  except:
    pass
  return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
  product = get_object_or_404(Products, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
      cart_item = CartItem.objects.get(product=product, cart=cart, id= cart_item_id)
    cart_item.delete()
  except:
    pass
  return redirect('cart')





@login_required(login_url='login')
def checkout(request, cart_items=None, total=0, tax=0, grand_total=0, shipping_cost = 0, quantity=0, cart_item=None):
  try:
    cart_items = CartItem.objects.filter(user=request.user, is_active =True).order_by('-created_date')
    for cart_item in cart_items:
          total += cart_item.sub_total()
          quantity += cart_item.quantity

    shipping_charge = ShippingCharge.objects.first()
    if total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    tax_percent = Tax.objects.first().tax_percentage
    

    tax = (tax_percent*total)/100

    grand_total = total+tax+shipping_cost
  
    addresses = Address.objects.filter(user=request.user, is_active=True).order_by('-date_added')
    
    send_mail(
      "Checiot For Product",
      f"There is a checkout request from {request.user.email}",
      None,
      ['phytomark6@gmail.com'],  
      fail_silently=False,
    )
    messages.warning(request, 'Please wait for us to approve your checkout before payment')

  except ObjectDoesNotExist:
    pass
  about = About.objects.first()
  info = Info.objects.first()
  context = {
    'about': about,
    'info': info,
    "total": total,
    "quantity" : quantity,
    "cart_items": cart_items,
    'shipping_cost': shipping_cost,
    'tax' : tax,
    'grand_total' : grand_total,
    'addresses': addresses
  }
  return render(request, 'product/checkout.html', context)


