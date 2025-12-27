from django.urls import path
from .views import (
    ShippingAddressListCreateView,
    ShippingAddressDetailView,
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderMarkAsPaidView,
)

app_name = 'orders'

urlpatterns = [
    # Shipping Addresses
    path('shipping-addresses/', ShippingAddressListCreateView.as_view(), name='shipping_address_list'),
    path('shipping-addresses/<int:pk>/', ShippingAddressDetailView.as_view(), name='shipping_address_detail'),
    
    # Orders
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/pay/', OrderMarkAsPaidView.as_view(), name='order_pay'),
]
