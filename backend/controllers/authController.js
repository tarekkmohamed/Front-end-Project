import User from '../models/User.js';
import { generateToken, generateActivationToken, generateResetPasswordToken } from '../middleware/auth.js';
import { sendActivationEmail, sendPasswordResetEmail } from '../utils/email.js';
import jwt from 'jsonwebtoken';

// @desc    Register a new user
// @route   POST /api/auth/register
// @access  Public
export const register = async (req, res) => {
    try {
        const { firstName, lastName, email, password, confirmPassword, mobilePhone, profilePicture } = req.body;

        // Validate input
        if (!firstName || !lastName || !email || !password || !confirmPassword || !mobilePhone) {
            return res.status(400).json({ message: 'Please provide all required fields' });
        }

        // Check if passwords match
        if (password !== confirmPassword) {
            return res.status(400).json({ message: 'Passwords do not match' });
        }

        // Check if user already exists
        const userExists = await User.findOne({ email });
        if (userExists) {
            return res.status(400).json({ message: 'User already exists with this email' });
        }

        // Generate activation token
        const activationToken = generateActivationToken(email);
        const activationTokenExpire = new Date(Date.now() + 24 * 60 * 60 * 1000); // 24 hours

        // Create user
        const user = await User.create({
            firstName,
            lastName,
            email,
            password,
            mobilePhone,
            profilePicture: profilePicture || null,
            activationToken,
            activationTokenExpire
        });

        if (user) {
            // Send activation email
            try {
                await sendActivationEmail(user.email, user.firstName, activationToken);
            } catch (error) {
                console.error('Failed to send activation email:', error);
                // Continue even if email fails
            }

            res.status(201).json({
                message: 'User registered successfully. Please check your email to activate your account.',
                user: {
                    id: user._id,
                    firstName: user.firstName,
                    lastName: user.lastName,
                    email: user.email,
                    mobilePhone: user.mobilePhone,
                    role: user.role
                }
            });
        } else {
            res.status(400).json({ message: 'Invalid user data' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error during registration' });
    }
};

// @desc    Activate user account
// @route   GET /api/auth/activate/:token
// @access  Public
export const activateAccount = async (req, res) => {
    try {
        const { token } = req.params;

        // Verify token
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        // Find user with this token
        const user = await User.findOne({
            email: decoded.id,
            activationToken: token,
            activationTokenExpire: { $gt: Date.now() }
        });

        if (!user) {
            return res.status(400).json({ message: 'Invalid or expired activation link' });
        }

        // Activate user
        user.isActive = true;
        user.activationToken = null;
        user.activationTokenExpire = null;
        await user.save();

        res.status(200).json({
            message: 'Account activated successfully. You can now login.',
            user: {
                id: user._id,
                email: user.email,
                firstName: user.firstName,
                lastName: user.lastName
            }
        });
    } catch (error) {
        console.error(error);
        if (error.name === 'JsonWebTokenError' || error.name === 'TokenExpiredError') {
            return res.status(400).json({ message: 'Invalid or expired activation link' });
        }
        res.status(500).json({ message: 'Server error during activation' });
    }
};

// @desc    Login user
// @route   POST /api/auth/login
// @access  Public
export const login = async (req, res) => {
    try {
        const { email, password } = req.body;

        // Validate input
        if (!email || !password) {
            return res.status(400).json({ message: 'Please provide email and password' });
        }

        // Find user by email (include password for comparison)
        const user = await User.findOne({ email }).select('+password');

        if (!user) {
            return res.status(401).json({ message: 'Invalid email or password' });
        }

        // Check if account is activated
        if (!user.isActive) {
            return res.status(401).json({ message: 'Please activate your account. Check your email for activation link.' });
        }

        // Check password
        const isPasswordValid = await user.comparePassword(password);

        if (!isPasswordValid) {
            return res.status(401).json({ message: 'Invalid email or password' });
        }

        // Generate token
        const token = generateToken(user._id);

        res.status(200).json({
            message: 'Login successful',
            token,
            user: {
                id: user._id,
                firstName: user.firstName,
                lastName: user.lastName,
                email: user.email,
                mobilePhone: user.mobilePhone,
                role: user.role,
                profilePicture: user.profilePicture
            }
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error during login' });
    }
};

// @desc    Request password reset
// @route   POST /api/auth/forgot-password
// @access  Public
export const forgotPassword = async (req, res) => {
    try {
        const { email } = req.body;

        if (!email) {
            return res.status(400).json({ message: 'Please provide email address' });
        }

        const user = await User.findOne({ email });

        if (!user) {
            // Don't reveal if user exists or not
            return res.status(200).json({ message: 'If the email exists, a password reset link has been sent.' });
        }

        // Generate reset token
        const resetToken = generateResetPasswordToken(user._id);
        const resetPasswordExpire = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

        user.resetPasswordToken = resetToken;
        user.resetPasswordExpire = resetPasswordExpire;
        await user.save();

        // Send reset email
        try {
            await sendPasswordResetEmail(user.email, user.firstName, resetToken);
        } catch (error) {
            console.error('Failed to send reset email:', error);
            user.resetPasswordToken = null;
            user.resetPasswordExpire = null;
            await user.save();
            return res.status(500).json({ message: 'Error sending email. Please try again.' });
        }

        res.status(200).json({ message: 'Password reset link has been sent to your email.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error during password reset request' });
    }
};

// @desc    Reset password
// @route   POST /api/auth/reset-password/:token
// @access  Public
export const resetPassword = async (req, res) => {
    try {
        const { token } = req.params;
        const { password, confirmPassword } = req.body;

        if (!password || !confirmPassword) {
            return res.status(400).json({ message: 'Please provide password and confirmation' });
        }

        if (password !== confirmPassword) {
            return res.status(400).json({ message: 'Passwords do not match' });
        }

        // Verify token
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        // Find user with this token
        const user = await User.findOne({
            _id: decoded.id,
            resetPasswordToken: token,
            resetPasswordExpire: { $gt: Date.now() }
        });

        if (!user) {
            return res.status(400).json({ message: 'Invalid or expired reset token' });
        }

        // Update password
        user.password = password;
        user.resetPasswordToken = null;
        user.resetPasswordExpire = null;
        await user.save();

        res.status(200).json({ message: 'Password has been reset successfully. You can now login.' });
    } catch (error) {
        console.error(error);
        if (error.name === 'JsonWebTokenError' || error.name === 'TokenExpiredError') {
            return res.status(400).json({ message: 'Invalid or expired reset token' });
        }
        res.status(500).json({ message: 'Server error during password reset' });
    }
};

// @desc    Get current user profile
// @route   GET /api/auth/profile
// @access  Private
export const getProfile = async (req, res) => {
    try {
        const user = await User.findById(req.user._id);

        if (user) {
            res.status(200).json({
                id: user._id,
                firstName: user.firstName,
                lastName: user.lastName,
                email: user.email,
                mobilePhone: user.mobilePhone,
                role: user.role,
                profilePicture: user.profilePicture,
                createdAt: user.createdAt
            });
        } else {
            res.status(404).json({ message: 'User not found' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching profile' });
    }
};

// @desc    Update user profile
// @route   PUT /api/auth/profile
// @access  Private
export const updateProfile = async (req, res) => {
    try {
        const user = await User.findById(req.user._id);

        if (user) {
            user.firstName = req.body.firstName || user.firstName;
            user.lastName = req.body.lastName || user.lastName;
            user.mobilePhone = req.body.mobilePhone || user.mobilePhone;
            user.profilePicture = req.body.profilePicture || user.profilePicture;

            // Update password if provided
            if (req.body.password) {
                user.password = req.body.password;
            }

            const updatedUser = await user.save();

            res.status(200).json({
                message: 'Profile updated successfully',
                user: {
                    id: updatedUser._id,
                    firstName: updatedUser.firstName,
                    lastName: updatedUser.lastName,
                    email: updatedUser.email,
                    mobilePhone: updatedUser.mobilePhone,
                    role: updatedUser.role,
                    profilePicture: updatedUser.profilePicture
                }
            });
        } else {
            res.status(404).json({ message: 'User not found' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error updating profile' });
    }
};
