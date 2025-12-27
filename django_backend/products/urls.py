from django.urls import path
from .views import (
    CategoryListView,
    TagListView,
    BrandListView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    SellerProductListView,
    FeaturedProductsView,
    LatestProductsView,
    ProductImageUploadView,
)

app_name = 'products'

urlpatterns = [
    # Categories, Tags, Brands
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('brands/', BrandListView.as_view(), name='brand_list'),
    
    # Products
    path('', ProductListView.as_view(), name='product_list'),
    path('featured/', FeaturedProductsView.as_view(), name='featured_products'),
    path('latest/', LatestProductsView.as_view(), name='latest_products'),
    path('seller/my-products/', SellerProductListView.as_view(), name='seller_products'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:product_id>/upload-image/', ProductImageUploadView.as_view(), name='product_image_upload'),
]
