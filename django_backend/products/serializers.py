from rest_framework import serializers
from .models import Category, Tag, Brand, Product, ProductImage
from reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    """Tag Serializer"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']


class BrandSerializer(serializers.ModelSerializer):
    """Brand Serializer"""
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    """Product Image Serializer"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Product List Serializer (for list views)"""
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    seller_name = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discounted_price', 'discount', 'stock_quantity',
                  'category', 'brand', 'seller_name', 'is_featured', 'average_rating',
                  'total_reviews', 'primary_image', 'created_at']
        read_only_fields = ['id', 'seller_name', 'average_rating', 'total_reviews', 'created_at']
    
    def get_seller_name(self, obj):
        return obj.seller.get_full_name()
    
    def get_discounted_price(self, obj):
        return float(obj.get_discounted_price())
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return self.context['request'].build_absolute_uri(primary_image.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Product Detail Serializer (for detail view)"""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    seller = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discounted_price', 'discount',
                  'stock_quantity', 'in_stock', 'category', 'tags', 'brand', 'seller',
                  'images', 'is_featured', 'average_rating', 'total_reviews',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'seller', 'average_rating', 'total_reviews',
                            'created_at', 'updated_at']
    
    def get_seller(self, obj):
        return {
            'id': obj.seller.id,
            'name': obj.seller.get_full_name(),
            'email': obj.seller.email
        }
    
    def get_discounted_price(self, obj):
        return float(obj.get_discounted_price())
    
    def get_in_stock(self, obj):
        return obj.is_in_stock()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Product Create/Update Serializer"""
    category_id = serializers.IntegerField(write_only=True)
    brand_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'discount', 'stock_quantity',
                  'category_id', 'brand_id', 'tag_ids']
    
    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid category ID.")
        return value
    
    def validate_brand_id(self, value):
        if value and not Brand.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid brand ID.")
        return value
    
    def validate_tag_ids(self, value):
        if value:
            existing_tags = Tag.objects.filter(id__in=value).count()
            if existing_tags != len(value):
                raise serializers.ValidationError("One or more invalid tag IDs.")
        return value
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        brand_id = validated_data.pop('brand_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        product = Product.objects.create(
            category_id=category_id,
            brand_id=brand_id,
            seller=self.context['request'].user,
            **validated_data
        )
        
        if tag_ids:
            product.tags.set(tag_ids)
        
        return product
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        brand_id = validated_data.pop('brand_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        if category_id:
            instance.category_id = category_id
        if brand_id is not None:
            instance.brand_id = brand_id
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        
        return instance
