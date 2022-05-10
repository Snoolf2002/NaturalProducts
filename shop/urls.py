from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import CatagoryViewSet, OrderListViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register('catagory', CatagoryViewSet)
router.register('product', ProductViewSet)
router.register('order', OrderViewSet)
router.register('order-list', OrderListViewSet)


urlpatterns = [
    path('', include(router.urls)),
]