from rest_framework import serializers

from shop.models import Product, Catagory, Order, catagory
from shop.models.order import OrderList


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ['id', 'title', 'image', 'descreption']


class ProductSerializer(serializers.ModelSerializer):
    # catagory = CatagorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'catagory', 'title', 'image', 'descreption', 'price', 'price_type', 'is_favorite', 'rating', 'order_amount']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'amount', 'payment']


class OrderListSerializer(serializers.ModelSerializer):
    # list = OrderSerializer(many=True)
    class Meta:
        model = OrderList
        fields = ['id', 'total_payment', 'list', 'order_time']