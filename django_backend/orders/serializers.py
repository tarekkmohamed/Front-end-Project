from rest_framework import serializers
from .models import ShippingAddress, Order, OrderItem
from products.models import Product


class ShippingAddressSerializer(serializers.ModelSerializer):
    """Shipping Address Serializer"""
    class Meta:
        model = ShippingAddress
        fields = ['id', 'full_name', 'phone_number', 'address_line1', 'address_line2',
                  'city', 'state', 'postal_code', 'country', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Order Item Serializer"""
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity', 'created_at']
        read_only_fields = ['id', 'product', 'product_title', 'product_price', 'created_at']
    
    def get_subtotal(self, obj):
        return float(obj.get_subtotal())


class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'total_amount', 'total_items',
                  'shipping_full_name', 'shipping_phone', 'shipping_address',
                  'shipping_city', 'shipping_country', 'shipping_postal_code',
                  'payment_method', 'is_paid', 'paid_at', 'is_delivered',
                  'delivered_at', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'items', 'created_at', 'updated_at']
    
    def get_total_items(self, obj):
        return obj.get_total_items()


class OrderCreateSerializer(serializers.Serializer):
    """Order Create Serializer"""
    shipping_address_id = serializers.IntegerField(required=False)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES)
    
    # Manual shipping address fields (if not using saved address)
    shipping_full_name = serializers.CharField(max_length=255, required=False)
    shipping_phone = serializers.CharField(max_length=20, required=False)
    shipping_address_line1 = serializers.CharField(max_length=255, required=False)
    shipping_address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    shipping_city = serializers.CharField(max_length=100, required=False)
    shipping_state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    shipping_postal_code = serializers.CharField(max_length=20, required=False)
    shipping_country = serializers.CharField(max_length=100, required=False)
    
    def validate(self, attrs):
        shipping_address_id = attrs.get('shipping_address_id')
        
        if not shipping_address_id:
            # Validate manual shipping address
            required_fields = ['shipping_full_name', 'shipping_phone', 'shipping_address_line1',
                               'shipping_city', 'shipping_postal_code', 'shipping_country']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(
                        f"{field} is required when not using a saved shipping address."
                    )
        
        return attrs
