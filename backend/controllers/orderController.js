import Order from '../models/Order.js';
import Cart from '../models/Cart.js';
import Product from '../models/Product.js';
import { sendOrderConfirmationEmail, sendOrderStatusEmail } from '../utils/email.js';

// @desc    Create new order
// @route   POST /api/orders
// @access  Private
export const createOrder = async (req, res) => {
    try {
        const { shippingAddress, paymentMethod } = req.body;

        // Validate shipping address
        if (!shippingAddress || !shippingAddress.address || !shippingAddress.city || 
            !shippingAddress.postalCode || !shippingAddress.country) {
            return res.status(400).json({ message: 'Please provide complete shipping address' });
        }

        // Get user's cart
        const cart = await Cart.findOne({ user: req.user._id }).populate('items.product');

        if (!cart || cart.items.length === 0) {
            return res.status(400).json({ message: 'Cart is empty' });
        }

        // Prepare order items and check stock
        const orderItems = [];
        let totalPrice = 0;

        for (const item of cart.items) {
            const product = await Product.findById(item.product._id);
            
            if (!product) {
                return res.status(404).json({ message: `Product ${item.product.title} not found` });
            }

            if (product.stock < item.quantity) {
                return res.status(400).json({ 
                    message: `Insufficient stock for ${product.title}. Available: ${product.stock}` 
                });
            }

            orderItems.push({
                product: product._id,
                title: product.title,
                quantity: item.quantity,
                price: product.price
            });

            totalPrice += product.price * item.quantity;

            // Update product stock
            product.stock -= item.quantity;
            await product.save();
        }

        // Create order
        const order = await Order.create({
            user: req.user._id,
            items: orderItems,
            shippingAddress,
            paymentMethod: paymentMethod || 'credit_card',
            totalPrice,
            status: 'pending'
        });

        // Clear cart after order
        cart.items = [];
        cart.totalPrice = 0;
        await cart.save();

        // Send confirmation email
        try {
            await sendOrderConfirmationEmail(req.user.email, req.user.firstName, order);
        } catch (error) {
            console.error('Failed to send order confirmation email:', error);
        }

        res.status(201).json({
            message: 'Order created successfully',
            order
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error creating order' });
    }
};

// @desc    Get user's orders
// @route   GET /api/orders/my-orders
// @access  Private
export const getMyOrders = async (req, res) => {
    try {
        const orders = await Order.find({ user: req.user._id })
            .populate('items.product', 'title images')
            .sort('-createdAt');

        res.status(200).json({
            orders,
            count: orders.length
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching orders' });
    }
};

// @desc    Get order by ID
// @route   GET /api/orders/:id
// @access  Private
export const getOrderById = async (req, res) => {
    try {
        const order = await Order.findById(req.params.id)
            .populate('user', 'firstName lastName email')
            .populate('items.product', 'title images');

        if (!order) {
            return res.status(404).json({ message: 'Order not found' });
        }

        // Check if user is authorized to view this order
        if (order.user._id.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
            return res.status(403).json({ message: 'Not authorized to view this order' });
        }

        res.status(200).json(order);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching order' });
    }
};

// @desc    Update order status (Admin only)
// @route   PUT /api/orders/:id/status
// @access  Private (Admin)
export const updateOrderStatus = async (req, res) => {
    try {
        const { status } = req.body;

        if (!status) {
            return res.status(400).json({ message: 'Status is required' });
        }

        const validStatuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
        if (!validStatuses.includes(status)) {
            return res.status(400).json({ message: 'Invalid status' });
        }

        const order = await Order.findById(req.params.id).populate('user', 'email firstName');

        if (!order) {
            return res.status(404).json({ message: 'Order not found' });
        }

        order.status = status;

        if (status === 'delivered') {
            order.isDelivered = true;
            order.deliveredAt = Date.now();
        }

        await order.save();

        // Send status update email
        try {
            await sendOrderStatusEmail(order.user.email, order.user.firstName, order);
        } catch (error) {
            console.error('Failed to send order status email:', error);
        }

        res.status(200).json({
            message: 'Order status updated',
            order
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error updating order status' });
    }
};

// @desc    Update order to paid (Simulated payment)
// @route   PUT /api/orders/:id/pay
// @access  Private
export const updateOrderToPaid = async (req, res) => {
    try {
        const order = await Order.findById(req.params.id);

        if (!order) {
            return res.status(404).json({ message: 'Order not found' });
        }

        // Check if user is authorized
        if (order.user.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
            return res.status(403).json({ message: 'Not authorized to update this order' });
        }

        order.isPaid = true;
        order.paidAt = Date.now();
        order.paymentResult = {
            id: req.body.id || 'simulated_payment_id',
            status: req.body.status || 'completed',
            update_time: req.body.update_time || Date.now(),
            email_address: req.body.email_address || req.user.email
        };
        order.status = 'processing';

        const updatedOrder = await order.save();

        res.status(200).json({
            message: 'Order marked as paid',
            order: updatedOrder
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error updating order' });
    }
};

// @desc    Get all orders (Admin only)
// @route   GET /api/orders
// @access  Private (Admin)
export const getAllOrders = async (req, res) => {
    try {
        const orders = await Order.find({})
            .populate('user', 'firstName lastName email')
            .populate('items.product', 'title')
            .sort('-createdAt');

        res.status(200).json({
            orders,
            count: orders.length
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching orders' });
    }
};
