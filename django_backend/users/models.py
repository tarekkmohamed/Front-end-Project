from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    
    # Override username to make email the primary login field
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=False)  # Requires email activation
    
    # Token fields for activation and password reset
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    activation_token_created = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    reset_password_token_created = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def is_activation_token_valid(self):
        """Check if activation token is still valid (24 hours)"""
        if not self.activation_token_created:
            return False
        expiry_time = self.activation_token_created + timedelta(hours=24)
        return timezone.now() < expiry_time
    
    def is_reset_password_token_valid(self):
        """Check if reset password token is still valid (1 hour)"""
        if not self.reset_password_token_created:
            return False
        expiry_time = self.reset_password_token_created + timedelta(hours=1)
        return timezone.now() < expiry_time


class UserProfile(models.Model):
    """
    User Profile model with OneToOne relationship to User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"Profile of {self.user.email}"
