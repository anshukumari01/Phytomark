from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Account
from django.contrib import messages, auth
from home.models import About
from home.models import Info
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.db.models import ProtectedError
from orders.models import Order, OrderDetails, OrderProduct, Payment
from django.core.paginator import Paginator
from product.models import Products

#varification
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.core.exceptions import ValidationError

import requests
import datetime

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
      # form = RegistrationForm()
      if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            company = form.cleaned_data["company"]
            country = form.cleaned_data["country"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name= first_name, last_name=last_name, email=email, username =username, password=password)
            user.phone_number = phone_number
            user.company = company
            user.country = country
            user.save()
            
            # user_profile =UserProfile.objects.create(user=user)
        
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'User approvel request'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
            })
            to_email = 'phytomark6@gmail.com'
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'Varification link has been sent to your email address. Please varify to continue ! ')
            return redirect('/accounts/login/?command=verification&email='+email)
      else:
        form = RegistrationForm()

      info = Info.objects.first()
      about = About.objects.first()
      context={
        'form': form,
        'info': info,
        'about': about,
        # 'user_profile': user_profile
      }
      return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            
            try:
               cart=Cart.objects.get(cart_id=_cart_id(request))
               is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
               if is_cart_item_exists:
                  cart_item = CartItem.objects.filter(cart=cart)

                  for item in cart_item:
                     item.user = user
                     item.save()
            except:
               pass
               
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                  next_page = params['next']
                  return redirect(next_page)
            except:
                return redirect('home')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid login crefentials!')
            return redirect('login')
        

    info = Info.objects.first()
    about = About.objects.first()
    context={
        'info': info,
        'about': about,
    }
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.warning(request,'You have been logged out successfully! ')
    return redirect('login')

def activate(request, uidb64, token):
    try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account .DoesNotExist):
      user = None

    if user is not None and default_token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      messages.success(request, 'Your account is activated successfully. You can login now !')
      return redirect('login')

    else:
      messages.error(request, 'Invalid activation link')
      return redirect('register')
    
@never_cache
def forgot_password(request):
  if request.method == 'POST':
    email = request.POST['email']
    if Account.objects.filter(email = email).exists():
      user = Account.objects.get(email__exact  =email)
      current_site = get_current_site(request)
      mail_subject = 'Reset password request'
      message = render_to_string('accounts/forgot-password-email.html',{
          'user' : user,
          'domain' : current_site,
          'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
          'token' : default_token_generator.make_token(user),
      })
      to_email = email
      send_email = EmailMessage(mail_subject, message, to=[to_email])
      send_email.send()

      messages.success(request, 'Password reset email has been send to your email address.')
      return redirect('login') 

    else:
      messages.error(request, 'No account is registered with email id you entered!')
      return redirect('forgot-password')

  return render(request, 'accounts/forgot-password.html')

@never_cache
def forgot_password_verify(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Account._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    return redirect('reset-password')
  else:
    messages.error(request, 'The link has been expired!')
    return redirect('login')


def reset_password(request):
  if request.method == 'POST':
    password = request.POST['new-password']
    confirm_password = request.POST['confirm-password']

    if password == confirm_password:
      uid = request.session.get('uid')
      user = Account.objects.get(pk=uid)
      user.set_password(password)
      user.save()
      request.session.pop('uid', None)
      messages.success(request, 'Password changed successfully.')
      print('Password changed successfully')
      return redirect('login')
    else:
      messages.error(request, 'Password do not match!')
      return redirect('reset-password')
  return render(request, 'accounts/reset-password.html')

@login_required(login_url='login')
def dashboard(request):
  info = Info.objects.first()
  about = About.objects.first()
  context = { 
     "info": info,
     "about": about
  }
  return render(request, 'accounts/dashboard.html', context)
  

@login_required(login_url='login')
def user_profile(request):
  change_password_form = ChangePasswordForm(user= request.user)
  info = Info.objects.first()
  about = About.objects.first()
  context = {
     'change_password_form':change_password_form,
     "info": info,
     "about": about
  }
  return render(request, 'accounts/profile.html',context)



@login_required(login_url='login')
def edit_profile(request):
  if request.method == 'POST':
    user_form = UserForm(request.POST, instance=request.user)
    if user_form.is_valid():
      user = UserForm()
      user.first_name = user_form.cleaned_data['first_name']
      user.last_name = user_form.cleaned_data['last_name']
      user.phone_number = user_form.cleaned_data['phone_number']
      user.date_of_birth = user_form.cleaned_data['date_of_birth']
      user_form.save()
      messages.success(request, 'Your Profile is updated successfuly')

  return redirect('user-profile')



@login_required(login_url='login')
def change_password(request):
  if request.method == 'POST':
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    check_current_password = request.user.check_password(current_password)
    print(check_current_password)
    if check_current_password:
      if new_password != confirm_password:
        messages.error(request, 'Passwords do not match!')
      else:
        try:
          validate_password(new_password)
          request.user.set_password(new_password)
          request.user.save()
          messages.success(request, 'Password changed successfully')
          print('Password changed successfully')
          return redirect('user-profile')

        except ValidationError as e:
          messages.error(request, str(e))
          print(str(e))
          return redirect('user-profile')
    else:
      messages.error(request, 'Make sure you entered old password correctly!')


  return redirect('user-profile')


@login_required(login_url='login')
def address(request):
  addresses = Address.objects.filter(user= request.user, is_active=True).order_by('-date_added')
  info = Info.objects.first()
  about = About.objects.first()
  context = {
    'addresses':addresses,
     "info": info,
     "about": about
  }
  return render(request, 'accounts/address.html', context)

@login_required(login_url='login')
def add_new_address(request):
  current_user = request.user
  if request.method == 'POST':
    form = AddressForm(request.POST)
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

      data.save()
      messages.success(request, 'New address is saved successfully')

  return redirect('user-address')

@login_required(login_url='login')
def delete_address(request, address_id):
  try:
    del_address = Address.objects.get(id = address_id)
    del_address.delete()
  except ProtectedError:
    del_address.is_active = False
    del_address.save()
  return redirect('user-address')

@login_required(login_url='login')
def edit_address(request, address_id):
  try:
    edit_address = Address.objects.get(id = address_id)
    if request.method == 'POST':
      edit_form = AddressForm(request.POST, instance= edit_address)
      if edit_form.is_valid():
        edit_form.save()
      else:
        messages.error(request, 'Invalid details')
  except:
    pass
  return redirect('user-address')

@login_required(login_url='login')
def orders(request):
  orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_date')
  order_products = OrderProduct.objects.filter(user=request.user, is_ordered=True).order_by('-created_date')
  order_details = OrderDetails.objects.filter(order__in=orders)

  if orders is not None:
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
  else:
    paged_orders = None
  info = Info.objects.first()
  about = About.objects.first()
  context = {
    'order_products':order_products,
    'orders':paged_orders,
    'order_details':order_details,
    'info':info,
    'about':about
  }
  return render(request, 'accounts/orders.html', context)

@login_required(login_url='login')
def order_details(request, order_id):
  order = None
  order_products =None
  try:
    order = get_object_or_404(Order, user=request.user,order_id=order_id, is_ordered=True)
    order_products = OrderProduct.objects.filter(user=request.user, order_id=order, is_ordered=True)
    order_details = OrderDetails.objects.filter(order=order)
  except (Order.DoesNotExist or OrderProduct.DoesNotExist):
    order = None
    order_products =None
  info = Info.objects.first()
  about = About.objects.first()
  context = {
    'order_products':order_products,
    'order':order,
    'order_details':order_details,
    'info':info,
    'about':about
  }
  return render(request, 'accounts/order-details.html', context)

@login_required(login_url='login')
def cancel_order(request, id):
  url = request.META.get('HTTP_REFERER')
  if request.method == "POST":
    order_note = request.POST['order_note']
    order_cancel = Order.objects.get(id=id)
    if order_cancel.status == 'Pending' or order_cancel.status == 'Placed' or order_cancel.status == 'Shipped':

      order_products = OrderProduct.objects.filter(order=order_cancel.id)
      for order_product in order_products:
        product = Products.objects.get(id=order_product.product_id)
        product.stock += order_product.quantity
        product.save()


      if order_cancel.status == 'Placed' or order_cancel.status == 'Shipped':
        payment = Payment.objects.get(id=order_cancel.payment.id)
        
      elif order_cancel.status == 'Pending':
        payment = Payment.objects.get(id=order_cancel.payment.id)
        payment.status = 'Failed'
        payment.save()

      order_cancel.status = 'Cancelled'
      order_cancel.save()
      

      # create order date object for the order
      OrderDetails.objects.create(
        order = order_cancel,
        order_status = order_cancel.status,
        note = order_note,
      )

      user = request.user
      message = render_to_string('orders/order-cancelled.html',{
        'user' : user,
        
      })
      send_mail(
          'One Order has been canclled',
           message,
           None,
           ['phytomark6@gmail.com'],
           fail_silently= False,
      )
      

      messages.warning(request, 'Order cancelled successfully')

    elif order_cancel.status == 'Out for Delivery':
      messages.error(request, "We cannot process cancellation request once the item is out for delivery, Please contact with the our courier partner or help center. If you dont want the product, Please don't recieve the product!")

  return redirect(url)

@login_required(login_url='login')
def return_order(request, id):
  url = request.META.get('HTTP_REFERER')
  if request.method == "POST":
    order_note = request.POST['order_note']
    order_cancel = Order.objects.get(id=id)
    if order_cancel.status == 'Delivered':


      order_cancel.status = 'Returned'
      order_cancel.save()
      
      


      # create order date object for the order
      OrderDetails.objects.create(
        order = order_cancel,
        order_status = order_cancel.status,
        note = order_note,
      )
      user = request.user
      message = render_to_string('orders/order-cancelled.html',{
        'user' : user,
      })
      send_mail(
          'One Order has been returned',
           message,
           None,
           ['phytomark6@gmail.com'],
           fail_silently= False,
      )
      messages.success(request, 'Return request recived')

  return redirect(url)

