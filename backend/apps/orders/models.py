from django.db import models
from django.conf import settings
from apps.food.models import FoodItem


class Order(models.Model):
    """Model representing a customer order"""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    # Delivery address
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_pincode = models.CharField(max_length=10)
    delivery_phone = models.CharField(max_length=15)
    delivery_name = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order #{self.id} by {self.user.name} - ₹{self.total_amount}"

    def update_status(self, new_status):
        """Update order status"""
        self.status = new_status
        if new_status == 'Delivered':
            from django.utils import timezone
            self.delivered_at = timezone.now()
        self.save()


class OrderItem(models.Model):
    """Model representing an item in an order"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name if self.food_item else 'Unknown'}"

    def save(self, *args, **kwargs):
        """Auto-calculate subtotal"""
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
