from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
import uuid
import logging

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer
)
from .utils.email import send_activation_email, send_password_reset_email

User = get_user_model()
logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """User Registration View"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send activation email
        try:
            send_activation_email(user, user.activation_token)
        except Exception as e:
            # Log error but don't fail registration
            logger.error(f"Error sending activation email: {e}")
        
        return Response({
            'message': 'User registered successfully. Please check your email to activate your account.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class AccountActivationView(APIView):
    """Account Activation View"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            user = User.objects.get(activation_token=token)
            
            if user.is_active:
                return Response({
                    'message': 'Account is already activated.'
                }, status=status.HTTP_200_OK)
            
            if not user.is_activation_token_valid():
                return Response({
                    'error': 'Activation link has expired.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.activation_token = None
            user.activation_token_created = None
            user.save()
            
            return Response({
                'message': 'Account activated successfully. You can now login.'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid activation link.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login View"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Please provide both email and password.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'error': 'Account is not activated. Please check your email.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        user_serializer = UserSerializer(user)
        
        return Response({
            'message': 'Login successful.',
            'user': user_serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logout View"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                # Try to blacklist the token if the feature is enabled
                try:
                    token.blacklist()
                except AttributeError:
                    # Blacklist feature not enabled, token will expire naturally
                    pass
            return Response({
                'message': 'Logout successful.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return Response({
                'error': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    """Password Reset Request View"""
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            user.reset_password_token = uuid.uuid4()
            user.reset_password_token_created = timezone.now()
            user.save()
            
            # Send password reset email
            try:
                send_password_reset_email(user, user.reset_password_token)
            except Exception as e:
                logger.error(f"Error sending password reset email: {e}")
        except User.DoesNotExist:
            # Don't reveal if email exists (security best practice)
            pass
        
        return Response({
            'message': 'If your email is registered, you will receive a password reset link.'
        }, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    """Password Reset View"""
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(reset_password_token=token)
            
            if not user.is_reset_password_token_valid():
                return Response({
                    'error': 'Password reset link has expired.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['password'])
            user.reset_password_token = None
            user.reset_password_token_created = None
            user.save()
            
            return Response({
                'message': 'Password reset successfully. You can now login with your new password.'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid password reset link.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User Profile View"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    """Change Password View"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)
