from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'user_name', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Review Create Serializer"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def create(self, validated_data):
        review = Review.objects.create(
            product=self.context['product'],
            user=self.context['request'].user,
            **validated_data
        )
        return review
