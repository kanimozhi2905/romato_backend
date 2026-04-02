from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from apps.cart.models import Cart


class PlaceOrderView(APIView):
    """Place a new order from cart"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            order = serializer.save()
            
            return Response({
                'success': True,
                'message': 'Order placed successfully',
                'data': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing orders"""
    
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.none()  # Will be overridden in get_queryset

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Order.objects.select_related('user').prefetch_related('items__food_item').all()
        return Order.objects.filter(user=user).select_related('user').prefetch_related('items__food_item').all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check permissions
        if not request.user.is_admin and instance.user != request.user:
            return Response({
                'success': False,
                'error': 'You do not have permission to view this order'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })


class UpdateOrderStatusView(APIView):
    """Update order status (Admin only)"""
    
    permission_classes = [IsAdminUser]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        new_status = request.data.get('status')

        if not new_status:
            return Response({
                'success': False,
                'error': 'Status is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = ['Pending', 'Preparing', 'Out for Delivery', 'Delivered', 'Cancelled']
        if new_status not in valid_statuses:
            return Response({
                'success': False,
                'error': f'Invalid status. Choose from: {", ".join(valid_statuses)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        order.update_status(new_status)

        return Response({
            'success': True,
            'message': f'Order status updated to {new_status}',
            'data': OrderSerializer(order).data
        }, status=status.HTTP_200_OK)


class UserOrdersView(generics.ListAPIView):
    """Get all orders for authenticated user"""
    
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
