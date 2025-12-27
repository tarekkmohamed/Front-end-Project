import express from 'express';
import {
    getAllUsers,
    getUserById,
    updateUser,
    deleteUser,
    getAllProductsAdmin,
    moderateProduct,
    getAnalytics,
    getSalesAnalytics
} from '../controllers/adminController.js';
import { protect, admin } from '../middleware/auth.js';

const router = express.Router();

// All admin routes require authentication and admin role
router.use(protect);
router.use(admin);

// User management
router.get('/users', getAllUsers);
router.get('/users/:id', getUserById);
router.put('/users/:id', updateUser);
router.delete('/users/:id', deleteUser);

// Product management
router.get('/products', getAllProductsAdmin);
router.put('/products/:id/moderate', moderateProduct);

// Analytics
router.get('/analytics', getAnalytics);
router.get('/analytics/sales', getSalesAnalytics);

export default router;
