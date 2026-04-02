from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['food_item', 'quantity', 'get_subtotal']
    fields = ['food_item', 'quantity', 'get_subtotal']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_items_count', 'get_total', 'created_at', 'updated_at']
    search_fields = ['user__name', 'user__email']
    ordering = ['-created_at']
    inlines = [CartItemInline]  # Show cart items in cart detail page


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'food_item', 'quantity', 'get_subtotal', 'added_at']
    list_filter = ['cart', 'food_item__category']
    search_fields = ['cart__user__name', 'food_item__name']
    ordering = ['-added_at']
