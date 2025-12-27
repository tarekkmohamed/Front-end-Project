from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    fields = ['product_title', 'product_price', 'quantity']
    readonly_fields = ['product_title', 'product_price', 'quantity']


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """Shipping Address Admin"""
    list_display = ['user', 'full_name', 'city', 'country', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'created_at']
    search_fields = ['user__email', 'full_name', 'city']
    ordering = ['-created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin"""
    list_display = ['order_number', 'user', 'status', 'total_amount', 'is_paid', 'is_delivered', 'created_at']
    list_filter = ['status', 'is_paid', 'is_delivered', 'created_at']
    search_fields = ['order_number', 'user__email']
    list_editable = ['status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_full_name', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_country', 'shipping_postal_code')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'is_paid', 'paid_at')
        }),
        ('Delivery Information', {
            'fields': ('is_delivered', 'delivered_at')
        }),
    )
    
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_processing(self, request, queryset):
        """Mark orders as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = 'Mark as Processing'
    
    def mark_as_shipped(self, request, queryset):
        """Mark orders as shipped"""
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = 'Mark as Shipped'
    
    def mark_as_delivered(self, request, queryset):
        """Mark orders as delivered"""
        from django.utils import timezone
        updated = queryset.update(status='delivered', is_delivered=True, delivered_at=timezone.now())
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = 'Mark as Delivered'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order Item Admin"""
    list_display = ['order', 'product_title', 'product_price', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product_title']
    ordering = ['-created_at']
