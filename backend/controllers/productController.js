import Product from '../models/Product.js';

// @desc    Get all products with filtering, search, and pagination
// @route   GET /api/products
// @access  Public
export const getProducts = async (req, res) => {
    try {
        const { 
            search, 
            category, 
            minPrice, 
            maxPrice, 
            rating,
            page = 1, 
            limit = 12,
            sort = '-createdAt',
            featured
        } = req.query;

        // Build query
        const query = { isActive: true };

        // Search by title or description
        if (search) {
            query.$or = [
                { title: { $regex: search, $options: 'i' } },
                { description: { $regex: search, $options: 'i' } }
            ];
        }

        // Filter by category
        if (category) {
            query.category = category;
        }

        // Filter by price range
        if (minPrice || maxPrice) {
            query.price = {};
            if (minPrice) query.price.$gte = Number(minPrice);
            if (maxPrice) query.price.$lte = Number(maxPrice);
        }

        // Filter by rating
        if (rating) {
            query.rating = { $gte: Number(rating) };
        }

        // Filter featured products
        if (featured === 'true') {
            query.isFeatured = true;
        }

        // Calculate pagination
        const pageNum = parseInt(page);
        const limitNum = parseInt(limit);
        const skip = (pageNum - 1) * limitNum;

        // Execute query
        const products = await Product.find(query)
            .populate('seller', 'firstName lastName email')
            .sort(sort)
            .limit(limitNum)
            .skip(skip);

        // Get total count
        const total = await Product.countDocuments(query);

        res.status(200).json({
            products,
            page: pageNum,
            pages: Math.ceil(total / limitNum),
            total,
            hasMore: skip + products.length < total
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching products' });
    }
};

// @desc    Get single product by ID
// @route   GET /api/products/:id
// @access  Public
export const getProductById = async (req, res) => {
    try {
        const product = await Product.findById(req.params.id)
            .populate('seller', 'firstName lastName email')
            .populate('reviews.user', 'firstName lastName');

        if (product) {
            res.status(200).json(product);
        } else {
            res.status(404).json({ message: 'Product not found' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching product' });
    }
};

// @desc    Create a product (Seller/Admin only)
// @route   POST /api/products
// @access  Private (Seller/Admin)
export const createProduct = async (req, res) => {
    try {
        const { title, description, price, category, images, stock } = req.body;

        // Validate required fields
        if (!title || !description || !price || !category) {
            return res.status(400).json({ message: 'Please provide all required fields' });
        }

        const product = await Product.create({
            title,
            description,
            price,
            category,
            images: images || [],
            stock: stock || 0,
            seller: req.user._id
        });

        res.status(201).json({
            message: 'Product created successfully',
            product
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error creating product' });
    }
};

// @desc    Update a product (Seller/Admin only)
// @route   PUT /api/products/:id
// @access  Private (Seller/Admin)
export const updateProduct = async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);

        if (!product) {
            return res.status(404).json({ message: 'Product not found' });
        }

        // Check if user is the seller or admin
        if (product.seller.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
            return res.status(403).json({ message: 'Not authorized to update this product' });
        }

        // Update fields
        product.title = req.body.title || product.title;
        product.description = req.body.description || product.description;
        product.price = req.body.price !== undefined ? req.body.price : product.price;
        product.category = req.body.category || product.category;
        product.images = req.body.images || product.images;
        product.stock = req.body.stock !== undefined ? req.body.stock : product.stock;

        const updatedProduct = await product.save();

        res.status(200).json({
            message: 'Product updated successfully',
            product: updatedProduct
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error updating product' });
    }
};

// @desc    Delete a product (Seller/Admin only)
// @route   DELETE /api/products/:id
// @access  Private (Seller/Admin)
export const deleteProduct = async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);

        if (!product) {
            return res.status(404).json({ message: 'Product not found' });
        }

        // Check if user is the seller or admin
        if (product.seller.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
            return res.status(403).json({ message: 'Not authorized to delete this product' });
        }

        await Product.findByIdAndDelete(req.params.id);

        res.status(200).json({ message: 'Product deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error deleting product' });
    }
};

// @desc    Get seller's products
// @route   GET /api/products/seller/my-products
// @access  Private (Seller/Admin)
export const getSellerProducts = async (req, res) => {
    try {
        const products = await Product.find({ seller: req.user._id });

        res.status(200).json({
            products,
            count: products.length
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching seller products' });
    }
};

// @desc    Add product review
// @route   POST /api/products/:id/reviews
// @access  Private
export const addProductReview = async (req, res) => {
    try {
        const { rating, comment } = req.body;

        if (!rating || !comment) {
            return res.status(400).json({ message: 'Please provide rating and comment' });
        }

        const product = await Product.findById(req.params.id);

        if (!product) {
            return res.status(404).json({ message: 'Product not found' });
        }

        // Check if user already reviewed
        const alreadyReviewed = product.reviews.find(
            review => review.user.toString() === req.user._id.toString()
        );

        if (alreadyReviewed) {
            return res.status(400).json({ message: 'Product already reviewed' });
        }

        const review = {
            user: req.user._id,
            name: `${req.user.firstName} ${req.user.lastName}`,
            rating: Number(rating),
            comment
        };

        product.reviews.push(review);
        product.numReviews = product.reviews.length;
        product.rating = product.reviews.reduce((acc, item) => item.rating + acc, 0) / product.reviews.length;

        await product.save();

        res.status(201).json({ message: 'Review added successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error adding review' });
    }
};

// @desc    Get featured/top-rated products
// @route   GET /api/products/featured/top
// @access  Public
export const getFeaturedProducts = async (req, res) => {
    try {
        const featured = await Product.find({ isFeatured: true, isActive: true })
            .limit(10)
            .sort('-rating');

        res.status(200).json(featured);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error fetching featured products' });
    }
};
