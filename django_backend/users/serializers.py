from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile
import uuid
from django.utils import timezone

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """User Profile Serializer"""
    class Meta:
        model = UserProfile
        fields = ['address', 'birthdate', 'city', 'country']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'mobile_phone', 'password', 'password2', 'role', 'profile']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def validate_role(self, value):
        # Only allow customer and seller roles during registration
        if value not in ['customer', 'seller']:
            raise serializers.ValidationError("Invalid role. Only 'customer' and 'seller' are allowed during registration.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        profile_data = validated_data.pop('profile', None)
        
        # Create user with activation token
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_phone=validated_data.get('mobile_phone', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'customer'),
            is_active=False,  # Requires email activation
            activation_token=uuid.uuid4(),
            activation_token_created=timezone.now()
        )
        
        # Create user profile
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    profile = UserProfileSerializer(required=False)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'mobile_phone', 
                  'profile_picture', 'role', 'is_active', 'profile', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile_phone = validated_data.get('mobile_phone', instance.mobile_phone)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        
        # Update profile
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password Reset Request Serializer"""
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    """Password Reset Serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Change Password Serializer"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True, label="Confirm New Password")
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
