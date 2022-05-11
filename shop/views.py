from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from shop.models import Catagory, Product, Order, OrderList
from shop.serializers import CatagorySerializer, OrderListSerializer, OrderSerializer, ProductSerializer
from users.models import MyUser


class CatagoryViewSet(ModelViewSet):
    queryset            = Catagory.objects.all()
    serializer_class    = CatagorySerializer
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['title']
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Catagory.objects.all()
    
    def perform_create(self, serializer):   
        user = self.request.user

        if user.is_staff:
            serializer.save()
            return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_staff:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer
    filter_backends     = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields       = ['title', 'catagory__title']
    ordering_fields     = ['rating', '-rating', 'order_amount', '-order_amount']
    filterset_fields    = ['catagory__title', 'catagory']
    pagination_class    = PageNumberPagination  

    @action(detail=True, methods=['POST'])
    def order(self, request, *args, **kwargs):
        product = self.get_object()

        with transaction.atomic():
            product.order_amount += 1
            product.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['POST'])
    def rate(self, request, *args, **kwargs):
        product = self.get_object()

        with transaction.atomic():
            product.rating_sum += request.data['rating']
            product.rating_amount += 1
            product.rating = product.rating_sum/product.rating_amount
            product.save()
        
        return Response({"rating": product.rating})

    @action(detail=True, methods=['POST'])
    def favourite(self, request, *args, **kwargs):
        user = self.request.user
        product = self.get_object()

        with transaction.atomic():
            user.favourite_fruites.add(product.id)
            user.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'])
    def favourites(self, request, *args, **kwargs):
        user = MyUser.objects.get(id=self.request.user.id)

        serializer = ProductSerializer(user.favourite_fruites.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def top(self, request, *args, **kwargs):

        top = Product.objects.all().order_by('-order_amount')[:4]
        serializer = self.get_serializer(top, many=True)
        
        return Response(serializer.data)

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_staff:
            serializer.save()


class OrderViewSet(ModelViewSet):
    queryset            = Order.objects.all()
    serializer_class    = OrderSerializer
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['product']
    pagination_class    = PageNumberPagination 

    def get_queryset(self):
        user = self.request.user

        if user:
            if user.is_staff:
                return Order.objects.all()
            else:
                return Order.objects.filter(user=user)
        else:
            return "You aren't register!"

    def perform_create(self, serializer):
        serializer.validated_data["user_id"] = self.request.user.id
        serializer.save()

    
class OrderListViewSet(ModelViewSet):
    queryset            = OrderList.objects.all()
    serializer_class    = OrderListSerializer
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['id']
    pagination_class    = PageNumberPagination 

    def get_queryset(self):
        user = self.request.user

        if user:
            if user.is_staff:
                return OrderList.objects.all()
            else:
                return OrderList.objects.filter(user=user)
        else:
            return "You aren't register!"

    def create(self, request, *args, **kwargs):
        orders = request.data
        user = self.request.user
        total_payment = 0

        if user:
            list_order = []
            for order in orders:
                new = Order.objects.create(
                    product  = Product.objects.get(id=order['product']),
                    amount   = order['amount'],
                    user = MyUser.objects.get(id = user.id)
                )
                new.save()
                
                total_payment += new.amount*new.product.price
                list_order.append(Order.objects.latest('id').id)
            

            serializer = self.get_serializer(data={
                    "list": list_order,
                    "total_payment": total_payment
                }
            )

            if serializer.is_valid():
                serializer.validated_data["user"] = self.request.user
                serializer.save()

                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)