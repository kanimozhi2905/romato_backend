from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.food.models import FoodItem


class CartView(generics.RetrieveAPIView):
    """Get user's cart"""
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(views.APIView):
    """Add item to cart or update quantity"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        food_item_id = request.data.get('food_item_id')
        quantity = request.data.get('quantity', 1)

        if not food_item_id:
            return Response({
                'success': False,
                'error': 'food_item_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get food item
        try:
            food_item = FoodItem.objects.get(id=food_item_id, is_available=True)
        except FoodItem.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Food item not found or unavailable'
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food_item=food_item,
            defaults={'quantity': quantity}
        )

        if not created:
            # If exists, update quantity
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({
            'success': True,
            'message': 'Item added to cart successfully',
            'data': CartSerializer(cart).data
        }, status=status.HTTP_200_OK)


class UpdateCartItemView(views.APIView):
    """Update quantity of cart item"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({
                'success': False,
                'error': 'quantity is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        quantity = int(quantity)

        if quantity <= 0:
            # Remove item if quantity is 0 or less
            cart_item.delete()
            message = 'Item removed from cart'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Cart item updated successfully'

        return Response({
            'success': True,
            'message': message,
            'data': CartSerializer(cart).data
        }, status=status.HTTP_200_OK)


class RemoveFromCartView(views.APIView):
    """Remove item from cart"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

        cart_item.delete()

        return Response({
            'success': True,
            'message': 'Item removed from cart successfully',
            'data': CartSerializer(cart).data
        }, status=status.HTTP_200_OK)


class ClearCartView(views.APIView):
    """Clear all items from cart"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()

        return Response({
            'success': True,
            'message': 'Cart cleared successfully'
        }, status=status.HTTP_200_OK)
