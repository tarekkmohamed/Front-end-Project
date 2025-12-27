# E-commerce Web Application

A comprehensive, secure, and scalable E-commerce platform with a React frontend and Node.js/Express backend.

## 🚀 Project Overview

This is a full-stack E-commerce application that provides a complete online shopping experience with features for customers, sellers, and administrators.

### Key Features

#### 🔐 Authentication System
- User registration with email validation
- Account activation via email (24-hour validity)
- Secure login with JWT authentication
- Password reset functionality
- User profile management

#### 🛍️ Product System
- Browse and search products with advanced filtering
- Product details with reviews and ratings
- Sellers can create, update, and delete their products
- Featured and top-rated product sections
- Category-based organization

#### 🛒 Shopping Cart & Orders
- Persistent shopping cart
- Smooth checkout process
- Order history and tracking
- Real-time order status updates
- Email notifications for order confirmation

#### 📊 Admin Panel
- User management (view, update, delete users)
- Product moderation and approval
- Sales analytics and dashboard
- Order management

#### 📱 Responsive Design
- Fully responsive for desktop, tablet, and mobile devices
- Modern UI with Material-UI components
- Smooth user experience

## 🏗️ Tech Stack

### Frontend
- **React 19** - UI library
- **Vite** - Build tool and dev server
- **Redux Toolkit** - State management
- **React Router** - Navigation
- **Material-UI** - UI components
- **Axios** - HTTP client
- **Bootstrap** - Styling framework

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MongoDB** - Database
- **Mongoose** - ODM
- **JWT** - Authentication
- **bcryptjs** - Password hashing
- **Nodemailer** - Email service
- **Helmet** - Security middleware
- **Express Rate Limit** - API protection

## 📦 Installation

### Prerequisites
- Node.js (v14 or higher)
- MongoDB (v4.4 or higher)
- npm or yarn

### Quick Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Front-end-Project
```

2. **Setup Backend**
```bash
# Run the setup script
./setup-backend.sh

# Or manually:
cd backend
npm install
cp .env.example .env
# Edit .env with your configuration
```

3. **Setup Frontend**
```bash
# From root directory
npm install
```

4. **Configure Environment Variables**

Edit `backend/.env` with your settings:
- MongoDB connection URI
- JWT secret key
- Email service credentials
- Frontend URL

5. **Start MongoDB**
```bash
mongod
```

6. **Start the Backend Server**
```bash
cd backend
npm run dev  # Development mode with auto-reload
# or
npm start    # Production mode
```

7. **Start the Frontend**
```bash
# From root directory
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 📖 Documentation

### Backend API Documentation
Detailed API documentation is available in [backend/README.md](backend/README.md)

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `GET /api/auth/activate/:token` - Activate account
- `POST /api/auth/login` - Login
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password/:token` - Reset password
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile

#### Products
- `GET /api/products` - Get all products (with filtering)
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Create product (Seller/Admin)
- `PUT /api/products/:id` - Update product (Seller/Admin)
- `DELETE /api/products/:id` - Delete product (Seller/Admin)
- `POST /api/products/:id/reviews` - Add review

#### Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart` - Add to cart
- `PUT /api/cart/:itemId` - Update cart item
- `DELETE /api/cart/:itemId` - Remove from cart

#### Orders
- `POST /api/orders` - Create order
- `GET /api/orders/my-orders` - Get user orders
- `GET /api/orders/:id` - Get order details
- `PUT /api/orders/:id/pay` - Mark as paid

#### Admin
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/:id` - Update user
- `DELETE /api/admin/users/:id` - Delete user
- `GET /api/admin/products` - Get all products
- `PUT /api/admin/products/:id/moderate` - Moderate product
- `GET /api/admin/analytics` - Get analytics

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Email verification for account activation
- Rate limiting on API endpoints
- CORS protection
- Helmet for security headers
- Role-based access control (Customer, Seller, Admin)

## 🎨 Project Structure

```
Front-end-Project/
├── backend/                 # Backend API
│   ├── config/             # Configuration files
│   ├── controllers/        # Request handlers
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   ├── middleware/        # Custom middleware
│   ├── utils/             # Utility functions
│   ├── server.js          # Entry point
│   └── README.md          # Backend documentation
├── src/                    # Frontend source
│   ├── components/        # React components
│   ├── screens/           # Page components
│   ├── store/             # Redux store
│   ├── constants/         # Constants
│   └── App.jsx            # Main app component
├── public/                # Static files
├── setup-backend.sh       # Backend setup script
└── README.md             # This file
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
npm test
```

### Frontend Testing
```bash
npm test
```

## 🚀 Deployment

### Backend Deployment
1. Set `NODE_ENV=production` in environment variables
2. Update MongoDB URI to production database
3. Configure email service for production
4. Deploy to your preferred platform (Heroku, AWS, DigitalOcean, etc.)

### Frontend Deployment
1. Build the frontend:
```bash
npm run build
```
2. Deploy the `dist` folder to your hosting service (Vercel, Netlify, etc.)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the ISC License.

## 👥 User Roles

### Customer
- Browse and search products
- Add items to cart
- Place orders
- Track order history
- Leave product reviews

### Seller
- All customer features
- Create and manage products
- View sales analytics
- Update product inventory

### Admin
- All seller features
- Manage all users
- Moderate products
- View comprehensive analytics
- Manage orders

## 🔧 Configuration

### Email Service Setup
For email functionality (activation, password reset, order notifications):
1. Use Gmail SMTP or any email service
2. Update `backend/.env` with credentials
3. For Gmail, enable "Less secure app access" or use App Passwords

### Database Setup
1. Install MongoDB locally or use MongoDB Atlas
2. Update `MONGODB_URI` in `backend/.env`
3. Database will be automatically created on first run

## 📞 Support

For issues or questions:
- Check the [Backend Documentation](backend/README.md)
- Review API endpoint examples
- Check logs for detailed error messages

## 🎯 Future Enhancements

Potential features for future development:
- Payment gateway integration (Stripe, PayPal)
- Social media authentication
- Advanced product recommendations
- Wishlist functionality
- Multi-vendor marketplace features
- Real-time notifications
- Advanced analytics dashboard
- Product comparison feature
- Live chat support

---

Built with ❤️ using React, Node.js, and MongoDB
