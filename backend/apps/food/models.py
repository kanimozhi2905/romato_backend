from django.db import models


class Category(models.Model):
    """Model for food categories"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """Model for individual food items"""
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    image = models.ImageField(upload_to='food_items/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_items'
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_available']),
        ]

    def __str__(self):
        return f"{self.name} - ₹{self.price}"
