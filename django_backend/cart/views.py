from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)


class CartView(APIView):
    """Get user's cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)


class AddToCartView(APIView):
    """Add item to cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get product
        product = get_object_or_404(Product, id=product_id, is_approved=True, is_active=True)
        
        # Check stock
        if product.stock_quantity < quantity:
            return Response({
                'error': f'Only {product.stock_quantity} items available in stock.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity
            new_quantity = cart_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return Response({
                    'error': f'Only {product.stock_quantity} items available in stock.'
                }, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity = new_quantity
            cart_item.save()
        
        cart_serializer = CartSerializer(cart, context={'request': request})
        return Response({
            'message': 'Item added to cart successfully.',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class UpdateCartItemView(APIView):
    """Update cart item quantity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity = serializer.validated_data['quantity']
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        # Check stock
        if cart_item.product.stock_quantity < quantity:
            return Response({
                'error': f'Only {cart_item.product.stock_quantity} items available in stock.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        cart_serializer = CartSerializer(cart_item.cart, context={'request': request})
        return Response({
            'message': 'Cart item updated successfully.',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class RemoveCartItemView(APIView):
    """Remove item from cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        
        cart_serializer = CartSerializer(cart, context={'request': request})
        return Response({
            'message': 'Item removed from cart successfully.',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    """Clear all items from cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            return Response({
                'message': 'Cart cleared successfully.'
            }, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({
                'message': 'Cart is already empty.'
            }, status=status.HTTP_200_OK)
