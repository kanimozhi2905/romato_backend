from rest_framework import serializers
from .models import Category, FoodItem


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    food_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'food_items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_food_items_count(self, obj):
        return obj.food_items.filter(is_available=True).count()


class FoodItemSerializer(serializers.ModelSerializer):
    """Serializer for FoodItem model with nested category"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = FoodItem
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_id',
            'image', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FoodItemListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing food items"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'category_name', 'image', 'is_available']
        read_only_fields = ['id']
