from rest_framework import serializers
from .models import Order, OrderItem
from apps.food.serializers import FoodItemListSerializer
from apps.food.models import FoodItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    food_item = FoodItemListSerializer(read_only=True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(),
        source='food_item',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'food_item_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'subtotal']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating OrderItems"""
    
    class Meta:
        model = OrderItem
        fields = ['food_item', 'quantity', 'price', 'subtotal']
        read_only_fields = ['subtotal']

    def create(self, validated_data):
        # Subtotal is auto-calculated in model save
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model with nested items"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'status', 'status_display',
            'delivery_address', 'delivery_city', 'delivery_pincode',
            'delivery_phone', 'delivery_name', 'items',
            'created_at', 'updated_at', 'delivered_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'delivered_at']


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for placing a new order"""
    
    delivery_address = serializers.CharField(required=True)
    delivery_city = serializers.CharField(required=True)
    delivery_pincode = serializers.CharField(required=True, max_length=10)
    delivery_phone = serializers.CharField(required=True, max_length=15)
    delivery_name = serializers.CharField(required=True, max_length=200)

    def validate_delivery_phone(self, value):
        if not value or len(value) < 10:
            raise serializers.ValidationError("Please provide a valid phone number")
        return value

    def create(self, validated_data):
        from apps.cart.models import Cart
        from django.utils import timezone
        
        user = self.context['request'].user
        
        # Get user's cart
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"error": "Cart is empty"})
        
        # Check if cart has items
        if not cart.items.exists():
            raise serializers.ValidationError({"error": "Cart is empty"})
        
        # Calculate total
        total_amount = cart.get_total()
        
        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                quantity=cart_item.quantity,
                price=cart_item.food_item.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return order
