from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from products.models import Product


class Cart(models.Model):
    """Shopping Cart Model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='carts',
        null=True,
        blank=True
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For guest users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        return f"Guest Cart {self.session_id}"
    
    def get_total(self):
        """Calculate total cart amount"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_items_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Cart Item Model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        unique_together = ['cart', 'product']  # One product per cart
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.product.get_discounted_price() * self.quantity
