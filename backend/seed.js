import mongoose from 'mongoose';
import dotenv from 'dotenv';
import User from './models/User.js';
import Product from './models/Product.js';
import connectDB from './config/db.js';

dotenv.config();

// Sample data
const users = [
    {
        firstName: 'Admin',
        lastName: 'User',
        email: 'admin@ecommerce.com',
        password: 'admin123',
        mobilePhone: '+1234567890',
        role: 'admin',
        isActive: true
    },
    {
        firstName: 'John',
        lastName: 'Seller',
        email: 'seller@ecommerce.com',
        password: 'seller123',
        mobilePhone: '+1234567891',
        role: 'seller',
        isActive: true
    },
    {
        firstName: 'Jane',
        lastName: 'Customer',
        email: 'customer@ecommerce.com',
        password: 'customer123',
        mobilePhone: '+1234567892',
        role: 'customer',
        isActive: true
    }
];

const products = [
    {
        title: 'Wireless Bluetooth Headphones',
        description: 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
        price: 99.99,
        category: 'electronics',
        images: ['https://via.placeholder.com/400'],
        stock: 50,
        rating: 4.5,
        isFeatured: true
    },
    {
        title: 'Smart Fitness Watch',
        description: 'Track your fitness goals with this advanced smartwatch featuring heart rate monitoring and GPS.',
        price: 199.99,
        category: 'electronics',
        images: ['https://via.placeholder.com/400'],
        stock: 30,
        rating: 4.7,
        isFeatured: true
    },
    {
        title: 'Cotton T-Shirt',
        description: 'Comfortable 100% cotton t-shirt available in multiple colors.',
        price: 19.99,
        category: 'clothing',
        images: ['https://via.placeholder.com/400'],
        stock: 100,
        rating: 4.2
    },
    {
        title: 'Running Shoes',
        description: 'Professional running shoes with excellent cushioning and support.',
        price: 79.99,
        category: 'sports',
        images: ['https://via.placeholder.com/400'],
        stock: 45,
        rating: 4.6
    },
    {
        title: 'Programming Book Set',
        description: 'Complete guide to modern web development with JavaScript and React.',
        price: 49.99,
        category: 'books',
        images: ['https://via.placeholder.com/400'],
        stock: 25,
        rating: 4.8,
        isFeatured: true
    },
    {
        title: 'Kitchen Blender',
        description: 'Powerful 1000W blender perfect for smoothies and food processing.',
        price: 89.99,
        category: 'home',
        images: ['https://via.placeholder.com/400'],
        stock: 20,
        rating: 4.4
    },
    {
        title: 'Yoga Mat',
        description: 'Non-slip yoga mat with extra cushioning for comfortable workouts.',
        price: 29.99,
        category: 'sports',
        images: ['https://via.placeholder.com/400'],
        stock: 60,
        rating: 4.3
    },
    {
        title: 'Wireless Mouse',
        description: 'Ergonomic wireless mouse with precision tracking.',
        price: 24.99,
        category: 'electronics',
        images: ['https://via.placeholder.com/400'],
        stock: 75,
        rating: 4.5
    }
];

const seedDatabase = async () => {
    try {
        // Connect to database
        await connectDB();

        console.log('Clearing existing data...');
        // Clear existing data
        await User.deleteMany({});
        await Product.deleteMany({});

        console.log('Creating users...');
        // Create users
        const createdUsers = await User.insertMany(users);
        console.log(`✓ Created ${createdUsers.length} users`);

        // Get the seller user
        const sellerUser = createdUsers.find(user => user.role === 'seller');

        // Add seller to products
        const productsWithSeller = products.map(product => ({
            ...product,
            seller: sellerUser._id
        }));

        console.log('Creating products...');
        // Create products
        const createdProducts = await Product.insertMany(productsWithSeller);
        console.log(`✓ Created ${createdProducts.length} products`);

        console.log('\n========================================');
        console.log('Database seeded successfully!');
        console.log('========================================');
        console.log('\nTest Accounts:');
        console.log('-------------------------------------------');
        console.log('Admin:');
        console.log('  Email: admin@ecommerce.com');
        console.log('  Password: admin123');
        console.log('\nSeller:');
        console.log('  Email: seller@ecommerce.com');
        console.log('  Password: seller123');
        console.log('\nCustomer:');
        console.log('  Email: customer@ecommerce.com');
        console.log('  Password: customer123');
        console.log('-------------------------------------------\n');

        process.exit(0);
    } catch (error) {
        console.error('Error seeding database:', error);
        process.exit(1);
    }
};

// Run the seed function
seedDatabase();
