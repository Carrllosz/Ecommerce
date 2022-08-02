from django.shortcuts import render, redirect
from django.http import JsonResponse
from .form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json


def home(request):
    products = Product.objects.filter(trending = 1)
    return render(request, 'home/index.html', {"products" : products})

def login_page(request):
  if request.user.is_authenticated:
    return redirect('/')
  else:
    if request.method == 'POST':
      name = request.POST.get('username')
      pwd = request.POST.get('password')
      user = authenticate(request, username = name, password = pwd)
      if user is not None:
        login(request, user)
        messages.success(request, 'Logged in successfully')
      else:
        messages.error(request, 'Invalid Username or Password')
        return redirect('/login/')

    return render(request, 'home/login.html')


def logout_view(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request, 'logged out successfully')
  return redirect('/')


def register(request):
  if request.method == 'POST':
    form = CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registration Success. You can login now!')
      return redirect('/login_page/')
  form = CustomUserForm()
  return render(request,'home/register.html',{'form' : form})


def collections(request):
    category = Category.objects.filter(status = 0)
    return render(request, 'home/collections.html', {'category' : category})


def collectionsview(request,name):
  if(Category.objects.filter(name = name,status=0)):
      products = Product.objects.filter(category__name=name)
      return render(request,"home/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
 
def product_details(request, cname, pname):
    if(Category.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"home/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')


def cart(request):
  if request.user.is_authenticated:
    cart = Cart.objects.filter(user = request.user)
    return render(request, 'home/cart.html', {"cart" : cart})

  else:
    return redirect('/login_page')


def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 

def remove_cart(request, cid):
  cart_item = Cart.objects.get(id = cid)
  cart_item.delete()
  return redirect('/cart')


def fav(request):
  if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
  else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def fav_view_page(request):
  if request.user_is_authenticated:
    fav = Favourite.objects.filter(user = request.user)
    return render(request, 'home/fav.html', {'fav':fav})
  else:
    return redirect('/')

def remove_fav(request, fid):
  item = Favourite.objects.get(id = id)
  item.delete()
  return redirect('/fav_view_page')