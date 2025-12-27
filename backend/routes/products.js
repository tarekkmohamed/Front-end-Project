import express from 'express';
import {
    getProducts,
    getProductById,
    createProduct,
    updateProduct,
    deleteProduct,
    getSellerProducts,
    addProductReview,
    getFeaturedProducts
} from '../controllers/productController.js';
import { protect, seller } from '../middleware/auth.js';

const router = express.Router();

// Public routes
router.get('/', getProducts);
router.get('/featured/top', getFeaturedProducts);

// Protected routes
router.post('/:id/reviews', protect, addProductReview);

// Seller/Admin routes - specific routes before parameterized routes
router.get('/seller/my-products', protect, seller, getSellerProducts);
router.post('/', protect, seller, createProduct);
router.put('/:id', protect, seller, updateProduct);
router.delete('/:id', protect, seller, deleteProduct);

// Parameterized route must come after specific routes
router.get('/:id', getProductById);

export default router;
