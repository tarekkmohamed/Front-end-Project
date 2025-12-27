import User from '../models/User.js';
import Product from '../models/Product.js';
import Order from '../models/Order.js';

// @desc    Get all users
// @route   GET /api/admin/users
// @access  Private (Admin)
export const getAllUsers = async (req, res) => {
    try {
        const users = await User.find({}).select('-password');

        res.status(200).json({
            users,
            count: users.length
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching users' });
    }
};

// @desc    Get user by ID
// @route   GET /api/admin/users/:id
// @access  Private (Admin)
export const getUserById = async (req, res) => {
    try {
        const user = await User.findById(req.params.id).select('-password');

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        res.status(200).json(user);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching user' });
    }
};

// @desc    Update user
// @route   PUT /api/admin/users/:id
// @access  Private (Admin)
export const updateUser = async (req, res) => {
    try {
        const user = await User.findById(req.params.id);

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        user.firstName = req.body.firstName || user.firstName;
        user.lastName = req.body.lastName || user.lastName;
        user.email = req.body.email || user.email;
        user.mobilePhone = req.body.mobilePhone || user.mobilePhone;
        user.role = req.body.role || user.role;
        user.isActive = req.body.isActive !== undefined ? req.body.isActive : user.isActive;

        const updatedUser = await user.save();

        res.status(200).json({
            message: 'User updated successfully',
            user: {
                id: updatedUser._id,
                firstName: updatedUser.firstName,
                lastName: updatedUser.lastName,
                email: updatedUser.email,
                mobilePhone: updatedUser.mobilePhone,
                role: updatedUser.role,
                isActive: updatedUser.isActive
            }
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error updating user' });
    }
};

// @desc    Delete user
// @route   DELETE /api/admin/users/:id
// @access  Private (Admin)
export const deleteUser = async (req, res) => {
    try {
        const user = await User.findById(req.params.id);

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Don't allow admin to delete themselves
        if (user._id.toString() === req.user._id.toString()) {
            return res.status(400).json({ message: 'Cannot delete your own account' });
        }

        await User.findByIdAndDelete(req.params.id);

        res.status(200).json({ message: 'User deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error deleting user' });
    }
};

// @desc    Get all products (Admin)
// @route   GET /api/admin/products
// @access  Private (Admin)
export const getAllProductsAdmin = async (req, res) => {
    try {
        const products = await Product.find({})
            .populate('seller', 'firstName lastName email');

        res.status(200).json({
            products,
            count: products.length
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching products' });
    }
};

// @desc    Moderate product (approve/reject/delete)
// @route   PUT /api/admin/products/:id/moderate
// @access  Private (Admin)
export const moderateProduct = async (req, res) => {
    try {
        const { action, isActive, isFeatured } = req.body;

        const product = await Product.findById(req.params.id);

        if (!product) {
            return res.status(404).json({ message: 'Product not found' });
        }

        if (action === 'delete') {
            await Product.findByIdAndDelete(req.params.id);
            return res.status(200).json({ message: 'Product deleted successfully' });
        }

        if (isActive !== undefined) {
            product.isActive = isActive;
        }

        if (isFeatured !== undefined) {
            product.isFeatured = isFeatured;
        }

        await product.save();

        res.status(200).json({
            message: 'Product moderated successfully',
            product
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error moderating product' });
    }
};

// @desc    Get analytics/dashboard stats
// @route   GET /api/admin/analytics
// @access  Private (Admin)
export const getAnalytics = async (req, res) => {
    try {
        // Get total counts
        const totalUsers = await User.countDocuments();
        const totalProducts = await Product.countDocuments();
        const totalOrders = await Order.countDocuments();

        // Get active users
        const activeUsers = await User.countDocuments({ isActive: true });

        // Get orders by status
        const pendingOrders = await Order.countDocuments({ status: 'pending' });
        const processingOrders = await Order.countDocuments({ status: 'processing' });
        const shippedOrders = await Order.countDocuments({ status: 'shipped' });
        const deliveredOrders = await Order.countDocuments({ status: 'delivered' });

        // Get total revenue
        const orders = await Order.find({ isPaid: true });
        const totalRevenue = orders.reduce((sum, order) => sum + order.totalPrice, 0);

        // Get recent orders
        const recentOrders = await Order.find({})
            .populate('user', 'firstName lastName email')
            .sort('-createdAt')
            .limit(10);

        // Get top products by orders
        const productStats = await Order.aggregate([
            { $unwind: '$items' },
            {
                $group: {
                    _id: '$items.product',
                    totalSold: { $sum: '$items.quantity' },
                    revenue: { $sum: { $multiply: ['$items.price', '$items.quantity'] } }
                }
            },
            { $sort: { totalSold: -1 } },
            { $limit: 10 }
        ]);

        // Populate product details
        const topProducts = await Product.populate(productStats, {
            path: '_id',
            select: 'title price images'
        });

        // Get seller statistics
        const sellerCount = await User.countDocuments({ role: 'seller' });
        const customerCount = await User.countDocuments({ role: 'customer' });

        res.status(200).json({
            overview: {
                totalUsers,
                activeUsers,
                totalProducts,
                totalOrders,
                totalRevenue,
                sellerCount,
                customerCount
            },
            orderStats: {
                pending: pendingOrders,
                processing: processingOrders,
                shipped: shippedOrders,
                delivered: deliveredOrders
            },
            recentOrders,
            topProducts
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching analytics' });
    }
};

// @desc    Get sales analytics
// @route   GET /api/admin/analytics/sales
// @access  Private (Admin)
export const getSalesAnalytics = async (req, res) => {
    try {
        const { period = 'month' } = req.query;

        let groupBy;
        let dateRange = new Date();

        if (period === 'week') {
            dateRange.setDate(dateRange.getDate() - 7);
            groupBy = { $dayOfYear: '$createdAt' };
        } else if (period === 'month') {
            dateRange.setMonth(dateRange.getMonth() - 1);
            groupBy = { $dayOfMonth: '$createdAt' };
        } else if (period === 'year') {
            dateRange.setFullYear(dateRange.getFullYear() - 1);
            groupBy = { $month: '$createdAt' };
        }

        const salesData = await Order.aggregate([
            {
                $match: {
                    createdAt: { $gte: dateRange },
                    isPaid: true
                }
            },
            {
                $group: {
                    _id: groupBy,
                    totalSales: { $sum: '$totalPrice' },
                    orderCount: { $sum: 1 }
                }
            },
            { $sort: { _id: 1 } }
        ]);

        res.status(200).json({
            period,
            salesData
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching sales analytics' });
    }
};
