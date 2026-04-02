from rest_framework import serializers
from .models import Cart, CartItem
from apps.food.serializers import FoodItemListSerializer
from apps.food.models import FoodItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    food_item = FoodItemListSerializer(read_only=True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(),
        source='food_item',
        write_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'food_item', 'food_item_id', 'quantity', 'subtotal', 'added_at']
        read_only_fields = ['id', 'added_at']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model with nested items"""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.get_total()

    def get_items_count(self, obj):
        return obj.get_items_count()
