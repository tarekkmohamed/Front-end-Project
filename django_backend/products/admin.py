from django.contrib import admin
from .models import Category, Tag, Brand, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images"""
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag Admin"""
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Brand Admin"""
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""
    list_display = ['title', 'seller', 'category', 'price', 'stock_quantity', 'is_approved', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_approved', 'is_featured', 'is_active', 'category', 'brand', 'created_at']
    search_fields = ['title', 'description', 'seller__email']
    list_editable = ['is_approved', 'is_featured', 'is_active']
    ordering = ['-created_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'brand', 'tags')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'discount', 'stock_quantity')
        }),
        ('Status', {
            'fields': ('seller', 'is_approved', 'is_featured', 'is_active')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['average_rating', 'total_reviews']
    
    actions = ['approve_products', 'feature_products', 'unfeature_products', 'deactivate_products']
    
    def approve_products(self, request, queryset):
        """Approve selected products"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} products were approved.')
    approve_products.short_description = 'Approve selected products'
    
    def feature_products(self, request, queryset):
        """Feature selected products"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products were featured.')
    feature_products.short_description = 'Feature selected products'
    
    def unfeature_products(self, request, queryset):
        """Unfeature selected products"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products were unfeatured.')
    unfeature_products.short_description = 'Unfeature selected products'
    
    def deactivate_products(self, request, queryset):
        """Deactivate selected products"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products were deactivated.')
    deactivate_products.short_description = 'Deactivate selected products'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Product Image Admin"""
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__title']
    ordering = ['-created_at']
