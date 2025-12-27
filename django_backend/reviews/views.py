from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ProductReviewListView(generics.ListAPIView):
    """List all reviews for a product"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id).order_by('-created_at')


class ProductReviewCreateView(generics.CreateAPIView):
    """Create a review for a product"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user already reviewed this product
        if Review.objects.filter(product=product, user=request.user).exists():
            return Response({
                'error': 'You have already reviewed this product.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'product': product}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        
        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )
