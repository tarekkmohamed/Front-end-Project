from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models import ShippingAddress, Order, OrderItem
from .serializers import (
    ShippingAddressSerializer,
    OrderSerializer,
    OrderCreateSerializer
)
from cart.models import Cart
from users.utils.email import send_order_confirmation_email


class ShippingAddressListCreateView(generics.ListCreateAPIView):
    """List and create shipping addresses"""
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShippingAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a shipping address"""
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)


class OrderCreateView(APIView):
    """Create an order from cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({
                'error': 'Cart is empty.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not cart.items.exists():
            return Response({
                'error': 'Cart is empty.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get shipping address
        shipping_address_id = serializer.validated_data.get('shipping_address_id')
        if shipping_address_id:
            shipping_address = get_object_or_404(
                ShippingAddress,
                id=shipping_address_id,
                user=request.user
            )
            shipping_data = {
                'shipping_full_name': shipping_address.full_name,
                'shipping_phone': shipping_address.phone_number,
                'shipping_address': f"{shipping_address.address_line1}\n{shipping_address.address_line2 or ''}".strip(),
                'shipping_city': shipping_address.city,
                'shipping_country': shipping_address.country,
                'shipping_postal_code': shipping_address.postal_code,
            }
        else:
            # Use manual shipping address
            shipping_data = {
                'shipping_full_name': serializer.validated_data['shipping_full_name'],
                'shipping_phone': serializer.validated_data['shipping_phone'],
                'shipping_address': f"{serializer.validated_data['shipping_address_line1']}\n{serializer.validated_data.get('shipping_address_line2', '')}".strip(),
                'shipping_city': serializer.validated_data['shipping_city'],
                'shipping_country': serializer.validated_data['shipping_country'],
                'shipping_postal_code': serializer.validated_data['shipping_postal_code'],
            }
        
        # Calculate total
        total_amount = cart.get_total()
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_method=serializer.validated_data['payment_method'],
            **shipping_data
        )
        
        # Create order items and update stock
        for cart_item in cart.items.all():
            # Check stock
            if cart_item.product.stock_quantity < cart_item.quantity:
                # Rollback transaction
                raise Exception(f'Insufficient stock for {cart_item.product.title}')
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_title=cart_item.product.title,
                product_price=cart_item.product.get_discounted_price(),
                quantity=cart_item.quantity
            )
            
            # Update stock
            cart_item.product.stock_quantity -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        # Send order confirmation email
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            print(f"Error sending order confirmation email: {e}")
        
        order_serializer = OrderSerializer(order)
        return Response({
            'message': 'Order created successfully.',
            'order': order_serializer.data
        }, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """List user's orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve order details"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderMarkAsPaidView(APIView):
    """Mark order as paid (simulated payment)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        
        if order.is_paid:
            return Response({
                'message': 'Order is already paid.'
            }, status=status.HTTP_200_OK)
        
        order.is_paid = True
        order.paid_at = timezone.now()
        order.save()
        
        order_serializer = OrderSerializer(order)
        return Response({
            'message': 'Order marked as paid successfully.',
            'order': order_serializer.data
        }, status=status.HTTP_200_OK)
