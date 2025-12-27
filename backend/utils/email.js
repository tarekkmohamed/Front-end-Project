import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

// Create reusable transporter
const transporter = nodemailer.createTransport({
    host: process.env.EMAIL_HOST,
    port: process.env.EMAIL_PORT,
    secure: process.env.EMAIL_PORT === '465', // true for 465, false for other ports
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD
    }
});

// Send activation email
export const sendActivationEmail = async (email, firstName, activationToken) => {
    const activationUrl = `${process.env.FRONTEND_URL}/activate/${activationToken}`;
    
    const mailOptions = {
        from: process.env.EMAIL_FROM,
        to: email,
        subject: 'Account Activation - E-commerce Platform',
        html: `
            <h2>Welcome to E-commerce Platform, ${firstName}!</h2>
            <p>Thank you for registering. Please click the link below to activate your account:</p>
            <a href="${activationUrl}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Activate Account</a>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account, please ignore this email.</p>
        `
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log('Activation email sent successfully');
    } catch (error) {
        console.error('Error sending activation email:', error);
        throw new Error('Failed to send activation email');
    }
};

// Send password reset email
export const sendPasswordResetEmail = async (email, firstName, resetToken) => {
    const resetUrl = `${process.env.FRONTEND_URL}/reset-password/${resetToken}`;
    
    const mailOptions = {
        from: process.env.EMAIL_FROM,
        to: email,
        subject: 'Password Reset - E-commerce Platform',
        html: `
            <h2>Password Reset Request</h2>
            <p>Hi ${firstName},</p>
            <p>You requested to reset your password. Click the link below to reset it:</p>
            <a href="${resetUrl}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request a password reset, please ignore this email.</p>
        `
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log('Password reset email sent successfully');
    } catch (error) {
        console.error('Error sending password reset email:', error);
        throw new Error('Failed to send password reset email');
    }
};

// Send order confirmation email
export const sendOrderConfirmationEmail = async (email, firstName, order) => {
    const mailOptions = {
        from: process.env.EMAIL_FROM,
        to: email,
        subject: 'Order Confirmation - E-commerce Platform',
        html: `
            <h2>Order Confirmation</h2>
            <p>Hi ${firstName},</p>
            <p>Thank you for your order! Your order has been received and is being processed.</p>
            <p><strong>Order ID:</strong> ${order._id}</p>
            <p><strong>Total Amount:</strong> $${order.totalPrice.toFixed(2)}</p>
            <p><strong>Status:</strong> ${order.status}</p>
            <p>You can track your order status in your account.</p>
        `
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log('Order confirmation email sent successfully');
    } catch (error) {
        console.error('Error sending order confirmation email:', error);
        // Don't throw error here as order is already created
    }
};

// Send order status update email
export const sendOrderStatusEmail = async (email, firstName, order) => {
    const mailOptions = {
        from: process.env.EMAIL_FROM,
        to: email,
        subject: 'Order Status Update - E-commerce Platform',
        html: `
            <h2>Order Status Update</h2>
            <p>Hi ${firstName},</p>
            <p>Your order status has been updated.</p>
            <p><strong>Order ID:</strong> ${order._id}</p>
            <p><strong>New Status:</strong> ${order.status}</p>
            <p>You can track your order in your account.</p>
        `
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log('Order status email sent successfully');
    } catch (error) {
        console.error('Error sending order status email:', error);
        // Don't throw error
    }
};
