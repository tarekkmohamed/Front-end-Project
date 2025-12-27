from django.urls import path
from .views import ProductReviewListView, ProductReviewCreateView

app_name = 'reviews'

urlpatterns = [
    path('products/<int:product_id>/reviews/', ProductReviewListView.as_view(), name='product_reviews'),
    path('products/<int:product_id>/reviews/create/', ProductReviewCreateView.as_view(), name='review_create'),
]
