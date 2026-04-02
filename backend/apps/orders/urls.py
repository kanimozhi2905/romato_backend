from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceOrderView, OrderViewSet, UpdateOrderStatusView, UserOrdersView

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Place order should come BEFORE the router to avoid conflicts
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/my-orders/', UserOrdersView.as_view(), name='my-orders'),
    path('orders/<int:order_id>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('', include(router.urls)),
]
