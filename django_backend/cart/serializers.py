from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Cart Item Serializer"""
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def get_subtotal(self, obj):
        return float(obj.get_subtotal())


class CartSerializer(serializers.ModelSerializer):
    """Cart Serializer"""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total(self, obj):
        return float(obj.get_total())
    
    def get_items_count(self, obj):
        return obj.get_items_count()


class AddToCartSerializer(serializers.Serializer):
    """Add to Cart Serializer"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Update Cart Item Serializer"""
    quantity = serializers.IntegerField(min_value=1)
