from django.shortcuts import render,redirect
from .forms import OrderForm
from accounts.models import Address
from carts.models import CartItem, ShippingCharge,Tax
from .models import *
from home.models import About
from home.models import Info

from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

from django.conf import settings

import string
import random
import datetime
import razorpay


# Create your views here.

def unique_id(size):
    chars = list(set(string.ascii_letters))
    return ''.join(random.choices(chars, k=size))

def save_address(request, total=0, tax=0, grand_total=0, shipping_cost = 0, quantity=0):
  current_user = request.user
  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      data = Address()
      data.user = current_user
      data.email = form.cleaned_data['email']
      data.mobile = form.cleaned_data['mobile']
      data.first_name = form.cleaned_data['first_name']
      data.last_name = form.cleaned_data['last_name']
      data.address = form.cleaned_data['address']
      data.landmark = form.cleaned_data['landmark']
      data.city = form.cleaned_data['city']
      data.pin_code = form.cleaned_data['pin_code']
      data.state = form.cleaned_data['state']
      data.country = form.cleaned_data['country']

      address = None
      existing_addresses = Address.objects.filter(user=current_user).order_by('-date_added')
      if existing_addresses is not None:
        for existing_address in existing_addresses:
          if data.__equal__(existing_address):
            print('Found Address in Existing address list')
            address = existing_address
            break

        if address is None:
          print('saved as a new address')
          data.save()
          address = Address.objects.get(user=current_user, id= data.id)
      else:
        print('none')
        data.save()


    addresses = Address.objects.filter(user=current_user, is_active=True).order_by('-date_added')

    cart_items = CartItem.objects.filter(user=current_user)
    for cart_item in cart_items:
      total += cart_item.sub_total()
      quantity += cart_item.quantity

    shipping_charge = ShippingCharge.objects.first()
    if total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    tax_percent = Tax.objects.first().tax_percentage
    

    tax = (tax_percent*total)/100
    grand_total = total+tax+shipping_cost
    
    
    info = Info.objects.first()
    about = About.objects.first()
    context = {
      'cart_items' : cart_items,
      'addresses': addresses,
      'shipping_charge': shipping_cost,
      'quantity' : quantity,
      'grand_total': grand_total,
      'tax': tax,
      'total':total,
      'info': info,
      'about': about
    }
    return render(request, 'orders/select-address.html', context)

  else:
    return redirect('checkout')

def payment_method(request, total=0, tax=0, grand_total=0, shipping_cost = 0, quantity=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  for cart_item in cart_items:
    if cart_item.quantity > cart_item.product.stock:
      out_of_stock = True
      break
    else:
      out_of_stock = False
  if cart_items_count <= 0 or out_of_stock:
    return redirect('cart')
  
  if request.method == "POST":

    address_id = request.POST.get('address')
    request.session['address_id'] = address_id

    for cart_item in cart_items:
      total += cart_item.sub_total()
      quantity += cart_item.quantity

    shipping_charge = ShippingCharge.objects.first()
    if total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge
    
    form = OrderForm(request.POST)
    if form.is_valid():
      country = form.cleaned_data['country']
    
      if country == 'india' or country == 'India':
        tax_percent = Tax.objects.first().tax_percentage
        tax = (tax_percent*total)/100
      else:
        tax = 0
    grand_total = total+tax+shipping_cost
    
    address = Address.objects.get(user=current_user, id=int(address_id))

    client = razorpay.Client (auth = (settings.KEY_ID, settings.SECRET_KEY) )
    payment = client.order.create({'amount' : grand_total*100, 'currency' : 'INR', 'payment_capture' : 1})
    print(payment)

    
    info = Info.objects.first()
    about = About.objects.first()
    context = {
      'cart_items' : cart_items,
      'address': address,
      'total': round(total),
      'shipping_charge': shipping_cost,
      'grand_total' : round(grand_total),
      'quantity' : quantity,
      'tax': tax,
      'info': info,
      'about': about,
      'payment' : payment
    }

    return render(request, 'orders/payment-method.html', context)


def payment(request, total=0, tax=0, grand_total=0, shipping_cost = 0, quantity=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  for cart_item in cart_items:
    if cart_item.quantity > cart_item.product.stock:
      out_of_stock = True
      break
    else:
      out_of_stock = False
  if cart_items_count <= 0 or out_of_stock:
    return redirect('cart')

  
  address_id = request.session['address_id']

  for cart_item in cart_items:
      total += cart_item.sub_total()
      quantity += cart_item.quantity

  shipping_charge = ShippingCharge.objects.first()
  if total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

  form = OrderForm(request.POST)
  if form.is_valid():
      country = form.cleaned_data['country']
    
      if country == 'india' or country == 'India':
        tax_percent = Tax.objects.first().tax_percentage
        tax = (tax_percent*total)/100
      else:
        tax = 0
  grand_total = total+tax+shipping_cost  
  
  client = razorpay.Client (auth = (settings.KEY_ID, settings.SECRET_KEY) )
  payment = client.order.create({'amount' : grand_total*100, 'currency' : 'INR', 'payment_capture' : 1})
  
  data = Order()

  ip_address = request.META.get('REMOTE_ADDR')
  address = Address.objects.get(user=current_user, id=int(address_id))

#   data.razor_pay_order_id = payment['id']
  data.user = current_user
  data.gross_amount = total
  data.shipping_charge = shipping_cost
  data.order_tax = tax
  data.order_total = grand_total
  data.address = address
  data.ip= ip_address
  data.save()

    # ORDER_ID 
  yr=int(datetime.date.today().strftime('%Y'))
  dt=int(datetime.date.today().strftime('%d'))
  mt=int(datetime.date.today().strftime('%m'))
  d=datetime.date(yr,mt,dt)
  current_date=d.strftime("%Y%m%d")
  order_id= str('OD000RBS') + current_date + str(data.id)
  data.order_id=order_id
  data.save()
  print(order_id)
    
  order = Order.objects.get(user=current_user, is_ordered=False, order_id=order_id)

  request.session['order_id'] = order_id
  
  payment= Payment()
  payment.user = current_user
  payment.amount = grand_total

  id =str(order.id)
  id_len=len(id)
  unique_id_generated = unique_id(11-id_len)
  payment_id= str(unique_id_generated) + id
  payment.payment_id= payment_id
  payment.status = 'Successful'
  payment.payment_method = 'razorpay'

  payment.save()
  
  order.is_ordered = True
  order.payment = payment
  order.status = 'Placed'
  order.save()

  


  cart_items = CartItem.objects.filter(user=request.user)

  order_products=[]
  for item in cart_items:
    orderproduct=OrderProduct()
    orderproduct.order = order
    orderproduct.payment=payment
    orderproduct.user=current_user
    orderproduct.product=item.product
    orderproduct.quantity=item.quantity
    orderproduct.price=item.product.price
    orderproduct.total = item.sub_total()
    orderproduct.gross_amount=item.sub_total()
    orderproduct.is_ordered=True
    orderproduct.save()

    cart_item=CartItem.objects.get(id=item.id)
    orderproduct=OrderProduct.objects.get(id=orderproduct.id)
    orderproduct.save()

    order_products.append(orderproduct.product.name)
      
      #reduce the quantity of ordered product from stock
    product = Products.objects.get(id=item.product_id)
    product.stock -= item.quantity
    product.save()

    #clear the cart items of the user
  CartItem.objects.filter(user=current_user).delete()

    # create order date object for the order
  OrderDetails.objects.create(
    order = order,
    order_status = order.status,
  )


    # delete data from session
  if order_id in request.session:
      del request.session['order_id']
      del request.session['address_id']

    # Send order recieved email to to the customer
  mail_subject = 'Your order has been successfully placed'
  message = render_to_string('orders/order-received-email-prepaid.html',{
      'user' : current_user,
      'product': order_products,
      'amount': order.order_total,
      'payment_id':payment_id,
      'address': order.address,
      'order_id': order.order_id,
      'order_date':order.updated_date,
  })
  to_email = current_user.email
  send_mail(mail_subject, message, 'phytomark6@gmail.com', [to_email], fail_silently=False)
    
  send_mail(
          'One Order has been placed',
           message,
           None,
           ['phytomark6@gmail.com'],
           fail_silently= False,
      )
  
  
  
    
  info = Info.objects.first()
  about = About.objects.first()
  context = {
    "info": info,
    "about" : about,
    'payment': payment
  }
  return render(request, 'orders/order-success.html', context)
    

def order_success(request):
    order_id = request.GET.get('order_id')
    try:
      order = Order.objects.get(order_id=order_id)
      context = {
        'order': order,
        'order_id':order_id
      }
      return render(request, 'orders/order-success.html', context)
    except Order.DoesNotExist:
      return redirect('home')

