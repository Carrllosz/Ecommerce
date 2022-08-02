from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('register', register, name='register'),
    path('login_page', login_page, name='login_page'),
    path('logout_view', logout_view, name='logout_view'),
    path('cart', cart, name='cart'),
    path('fav', fav, name='fav'),
    path('fav_view_page', fav_view_page, name='fav_view_page'),
    path('remove_path/<str:cid>', remove_fav, name='remove_fav'),
    path('remove_cart/<str:cid>', remove_cart, name='remove_cart'),
    path('collections', collections , name='collections'),
    path('collections/<str:name>', collectionsview, name='collections'),
    path('collections/<str:cname>/<str:pname>', product_details, name='product_details'),
    path('addtocart', add_to_cart, name='addtocart'),

]