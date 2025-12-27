from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Category, Tag, Brand, Product, ProductImage
from .serializers import (
    CategorySerializer,
    TagSerializer,
    BrandSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer
)


class IsSellerOrAdmin(permissions.BasePermission):
    """Permission class for sellers and admins"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['seller', 'admin']


class IsProductOwnerOrAdmin(permissions.BasePermission):
    """Permission class for product owner or admin"""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.seller == request.user


# Category Views
class CategoryListView(generics.ListAPIView):
    """List all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# Tag Views
class TagListView(generics.ListAPIView):
    """List all tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


# Brand Views
class BrandListView(generics.ListAPIView):
    """List all brands"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]


# Product Views
class ProductListView(generics.ListAPIView):
    """List all products with filtering and search"""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'average_rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_approved=True, is_active=True)
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by brand
        brand_id = self.request.query_params.get('brand')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        
        # Filter by tag
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        
        # Filter featured products
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve a single product"""
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Product.objects.filter(is_approved=True, is_active=True)


class ProductCreateView(generics.CreateAPIView):
    """Create a new product"""
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsSellerOrAdmin]


class ProductUpdateView(generics.UpdateAPIView):
    """Update a product"""
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsProductOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Product.objects.all()
        return Product.objects.filter(seller=self.request.user)


class ProductDeleteView(generics.DestroyAPIView):
    """Delete a product"""
    permission_classes = [IsProductOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Product.objects.all()
        return Product.objects.filter(seller=self.request.user)


class SellerProductListView(generics.ListAPIView):
    """List products for the logged-in seller"""
    serializer_class = ProductListSerializer
    permission_classes = [IsSellerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Product.objects.all()
        return Product.objects.filter(seller=self.request.user)


class FeaturedProductsView(generics.ListAPIView):
    """List featured and top-rated products"""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Product.objects.filter(
            is_approved=True,
            is_active=True,
            is_featured=True
        ).order_by('-average_rating', '-created_at')[:10]


class LatestProductsView(generics.ListAPIView):
    """List latest products"""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Product.objects.filter(
            is_approved=True,
            is_active=True
        ).order_by('-created_at')[:20]


class ProductImageUploadView(APIView):
    """Upload product images"""
    permission_classes = [IsProductOwnerOrAdmin]
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        # Check permission
        if request.user.role != 'admin' and product.seller != request.user:
            return Response({
                'error': 'You do not have permission to upload images for this product.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        image = request.FILES.get('image')
        is_primary = request.data.get('is_primary', False)
        
        if not image:
            return Response({
                'error': 'No image provided.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        product_image = ProductImage.objects.create(
            product=product,
            image=image,
            is_primary=is_primary
        )
        
        serializer = ProductImageSerializer(product_image, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
