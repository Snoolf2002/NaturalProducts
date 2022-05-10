from django.contrib import admin
from shop.models.catagory import Catagory
from shop.models.order import Order, OrderList

from shop.models.product import Product


admin.site.register([Product, Catagory, Order, OrderList])