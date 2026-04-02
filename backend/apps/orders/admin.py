from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['food_item', 'quantity', 'price', 'subtotal']
    fields = ['food_item', 'quantity', 'price', 'subtotal']
    
    def subtotal(self, obj):
        return obj.get_subtotal()
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'delivery_name', 'total_amount', 'status', 
        'items_count', 'created_at', 'delivered_at'
    ]
    list_filter = ['status', 'created_at', 'delivered_at']
    search_fields = ['delivery_name', 'delivery_phone', 'user__name', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'delivered_at', 'total_amount']
    list_editable = ['status']  # Allow quick status change from list view
    inlines = [OrderItemInline]  # Show order items in order detail page
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'total_amount', 'status')
        }),
        ('Delivery Details', {
            'fields': ('delivery_name', 'delivery_address', 'delivery_city', 
                      'delivery_pincode', 'delivery_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Add action buttons for quick status updates
    actions = ['mark_as_pending', 'mark_as_preparing', 'mark_as_out_for_delivery', 
               'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='Pending')
        self.message_user(request, f'{updated} orders marked as Pending.')
    mark_as_pending.short_description = 'Mark selected orders as Pending'
    
    def mark_as_preparing(self, request, queryset):
        updated = queryset.update(status='Preparing')
        self.message_user(request, f'{updated} orders marked as Preparing.')
    mark_as_preparing.short_description = 'Mark selected orders as Preparing'
    
    def mark_as_out_for_delivery(self, request, queryset):
        updated = queryset.update(status='Out for Delivery')
        self.message_user(request, f'{updated} orders marked as Out for Delivery.')
    mark_as_out_for_delivery.short_description = 'Mark selected orders as Out for Delivery'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='Delivered')
        self.message_user(request, f'{updated} orders marked as Delivered.')
    mark_as_delivered.short_description = 'Mark selected orders as Delivered'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f'{updated} orders marked as Cancelled.')
    mark_as_cancelled.short_description = 'Mark selected orders as Cancelled'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'food_item', 'quantity', 'price', 'subtotal']
    list_filter = ['order__status', 'food_item__category']
    search_fields = ['order__delivery_name', 'food_item__name']
    ordering = ['-order__created_at']
