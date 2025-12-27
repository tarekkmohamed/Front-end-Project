from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin"""
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__email', 'product__title', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
