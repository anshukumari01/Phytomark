
# Create your views here.
from django.shortcuts import render,get_object_or_404, redirect
from home.models import About
from home.models import Info
from django.db.models import Q

from carts.models import ShippingCharge
from django.contrib import messages
from .models import Products
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def products(request):
    products = None
    products = Products.objects.filter(is_available=True).order_by('-modified_date')

    if products is not None:
        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        paged_products = None

    product_count = products.count()
    about = About.objects.first()
    info = Info.objects.first()

    context={
        'about': about,
        'info': info,
        'products' : paged_products,
        'product_count': product_count,
    }
    return render(request, 'product/products.html', context)


def search(request):
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword :
      products = Products.objects.filter(
          Q(name__icontains=keyword) | 
          Q(cas_number__icontains=keyword) |
          Q(cat_number__icontains=keyword) 
        ).order_by('-modified_date')
      product_count = products.count()

      paginator = Paginator(products, 5)
      page = request.GET.get('page')
      paged_products = paginator.get_page(page)

    else:
      products = Products.objects.all().order_by('-modified_date')
      product_count = products.count()
      paginator = Paginator(products, 5)
      page = request.GET.get('page')
      paged_products = paginator.get_page(page)

  
  about = About.objects.first()
  info = Info.objects.first()
  
  context = {
    'about': about,
    'info': info,
    'products' : paged_products ,
    'product_count': product_count,
    'keyword' : keyword
  }
  return render(request, 'product/products.html', context)

def product_view(request, product_slug=None):
  about = About.objects.first()
  info = Info.objects.first()
  product = Products.objects.get(slug=product_slug)

  free_shipping_price = ShippingCharge.objects.first().range_upto
  context = {
    'product': product,
    'about': about,
    'info': info,
    'free_shipping_price':free_shipping_price,
    
  }
  return render(request, 'product/product-view.html', context)
