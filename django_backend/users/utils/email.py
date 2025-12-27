from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_email(user, token):
    """Send account activation email"""
    activation_url = f"{settings.FRONTEND_URL}/activate/{token}"
    
    subject = 'Activate Your E-commerce Account'
    html_message = f"""
    <html>
        <body>
            <h2>Welcome to our E-commerce Platform!</h2>
            <p>Hi {user.first_name},</p>
            <p>Thank you for registering. Please click the link below to activate your account:</p>
            <p><a href="{activation_url}">{activation_url}</a></p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account, please ignore this email.</p>
            <br>
            <p>Best regards,<br>E-commerce Team</p>
        </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, token):
    """Send password reset email"""
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
    
    subject = 'Password Reset Request'
    html_message = f"""
    <html>
        <body>
            <h2>Password Reset</h2>
            <p>Hi {user.first_name},</p>
            <p>We received a request to reset your password. Click the link below to reset it:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request a password reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>E-commerce Team</p>
        </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_order_confirmation_email(order):
    """Send order confirmation email"""
    subject = f'Order Confirmation - {order.order_number}'
    html_message = f"""
    <html>
        <body>
            <h2>Order Confirmation</h2>
            <p>Hi {order.user.first_name},</p>
            <p>Thank you for your order! Your order has been received and is being processed.</p>
            <p><strong>Order Number:</strong> {order.order_number}</p>
            <p><strong>Total Amount:</strong> ${order.total_amount}</p>
            <p><strong>Shipping Address:</strong><br>
            {order.shipping_full_name}<br>
            {order.shipping_address}<br>
            {order.shipping_city}, {order.shipping_country}</p>
            <p>You can track your order status in your account.</p>
            <br>
            <p>Best regards,<br>E-commerce Team</p>
        </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_order_status_email(order):
    """Send order status update email"""
    subject = f'Order Status Update - {order.order_number}'
    html_message = f"""
    <html>
        <body>
            <h2>Order Status Update</h2>
            <p>Hi {order.user.first_name},</p>
            <p>Your order status has been updated.</p>
            <p><strong>Order Number:</strong> {order.order_number}</p>
            <p><strong>Current Status:</strong> {order.get_status_display()}</p>
            <p>You can view your order details in your account.</p>
            <br>
            <p>Best regards,<br>E-commerce Team</p>
        </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        html_message=html_message,
        fail_silently=False,
    )
