from django.db import models
from django.conf import settings
from apps.food.models import FoodItem


class Cart(models.Model):
    """Model representing a user's cart"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart for {self.user.name}"

    def get_total(self):
        """Calculate total price of all items in cart"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_items_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Model representing an item in the cart"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'food_item']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.food_item.price * self.quantity
