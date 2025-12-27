from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items"""
    model = CartItem
    extra = 0
    fields = ['product', 'quantity']
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart Admin"""
    list_display = ['id', 'user', 'session_id', 'get_items_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'session_id']
    ordering = ['-updated_at']
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.get_items_count()
    get_items_count.short_description = 'Items Count'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Cart Item Admin"""
    list_display = ['cart', 'product', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['product__title', 'cart__user__email']
    ordering = ['-added_at']
