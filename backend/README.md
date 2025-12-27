# E-commerce Backend API

A comprehensive backend system for an E-commerce Web Application built with Node.js, Express, and MongoDB.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Security Features](#security-features)

## Features

### Authentication System
- User registration with email validation
- Email account activation (24-hour validity)
- Secure login with JWT tokens
- Password reset via email
- Profile management

### Product System
- CRUD operations for sellers
- Product browsing with search and filters
- Pagination support
- Product reviews and ratings
- Featured products

### Cart & Order System
- Persistent shopping cart
- Checkout process
- Order history and tracking
- Order status updates
- Email notifications

### Admin Panel
- User management
- Product moderation
- Sales analytics
- Dashboard statistics

## Tech Stack

- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: MongoDB with Mongoose
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcryptjs
- **Email**: Nodemailer
- **Security**: Helmet, express-rate-limit
- **Validation**: express-validator

## Installation

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start MongoDB** (if running locally):
```bash
mongod
```

5. **Run the server**:
```bash
# Development mode with auto-restart
npm run dev

# Production mode
npm start
```

The server will start on `http://localhost:5000`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# Database Configuration
MONGODB_URI=mongodb://localhost:27017/ecommerce

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRE=7d
JWT_ACTIVATION_EXPIRE=24h
JWT_RESET_PASSWORD_EXPIRE=1h

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
EMAIL_FROM=noreply@ecommerce.com

# Frontend URL
FRONTEND_URL=http://localhost:5173

# File Upload
MAX_FILE_SIZE=5242880
UPLOAD_PATH=./uploads
```

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "confirmPassword": "password123",
  "mobilePhone": "+1234567890",
  "profilePicture": "url_optional"
}
```

#### Activate Account
```http
GET /api/auth/activate/:token
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

#### Forgot Password
```http
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "john@example.com"
}
```

#### Reset Password
```http
POST /api/auth/reset-password/:token
Content-Type: application/json

{
  "password": "newpassword123",
  "confirmPassword": "newpassword123"
}
```

#### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer <token>
```

#### Update Profile
```http
PUT /api/auth/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Smith",
  "mobilePhone": "+1234567890"
}
```

### Product Endpoints

#### Get All Products
```http
GET /api/products?page=1&limit=12&search=laptop&category=electronics&minPrice=100&maxPrice=1000
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 12)
- `search`: Search term
- `category`: Filter by category
- `minPrice`: Minimum price
- `maxPrice`: Maximum price
- `rating`: Minimum rating
- `featured`: Get featured products (true/false)
- `sort`: Sort field (default: -createdAt)

#### Get Featured Products
```http
GET /api/products/featured/top
```

#### Get Product by ID
```http
GET /api/products/:id
```

#### Create Product (Seller/Admin)
```http
POST /api/products
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "category": "electronics",
  "images": ["url1", "url2"],
  "stock": 10
}
```

#### Update Product (Seller/Admin)
```http
PUT /api/products/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Name",
  "price": 89.99,
  "stock": 15
}
```

#### Delete Product (Seller/Admin)
```http
DELETE /api/products/:id
Authorization: Bearer <token>
```

#### Get Seller's Products
```http
GET /api/products/seller/my-products
Authorization: Bearer <token>
```

#### Add Product Review
```http
POST /api/products/:id/reviews
Authorization: Bearer <token>
Content-Type: application/json

{
  "rating": 5,
  "comment": "Great product!"
}
```

### Cart Endpoints

#### Get Cart
```http
GET /api/cart
Authorization: Bearer <token>
```

#### Add to Cart
```http
POST /api/cart
Authorization: Bearer <token>
Content-Type: application/json

{
  "productId": "product_id_here",
  "quantity": 2
}
```

#### Update Cart Item
```http
PUT /api/cart/:itemId
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 3
}
```

#### Remove from Cart
```http
DELETE /api/cart/:itemId
Authorization: Bearer <token>
```

#### Clear Cart
```http
DELETE /api/cart
Authorization: Bearer <token>
```

### Order Endpoints

#### Create Order
```http
POST /api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "shippingAddress": {
    "address": "123 Main St",
    "city": "New York",
    "postalCode": "10001",
    "country": "USA"
  },
  "paymentMethod": "credit_card"
}
```

#### Get My Orders
```http
GET /api/orders/my-orders
Authorization: Bearer <token>
```

#### Get Order by ID
```http
GET /api/orders/:id
Authorization: Bearer <token>
```

#### Update Order to Paid
```http
PUT /api/orders/:id/pay
Authorization: Bearer <token>
Content-Type: application/json

{
  "id": "payment_id",
  "status": "completed"
}
```

#### Get All Orders (Admin)
```http
GET /api/orders
Authorization: Bearer <admin_token>
```

#### Update Order Status (Admin)
```http
PUT /api/orders/:id/status
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "status": "shipped"
}
```
Status options: pending, processing, shipped, delivered, cancelled

### Admin Endpoints

#### Get All Users
```http
GET /api/admin/users
Authorization: Bearer <admin_token>
```

#### Get User by ID
```http
GET /api/admin/users/:id
Authorization: Bearer <admin_token>
```

#### Update User
```http
PUT /api/admin/users/:id
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "role": "seller",
  "isActive": true
}
```

#### Delete User
```http
DELETE /api/admin/users/:id
Authorization: Bearer <admin_token>
```

#### Get All Products (Admin)
```http
GET /api/admin/products
Authorization: Bearer <admin_token>
```

#### Moderate Product
```http
PUT /api/admin/products/:id/moderate
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "isActive": true,
  "isFeatured": true
}
```

Or to delete:
```json
{
  "action": "delete"
}
```

#### Get Analytics
```http
GET /api/admin/analytics
Authorization: Bearer <admin_token>
```

#### Get Sales Analytics
```http
GET /api/admin/analytics/sales?period=month
Authorization: Bearer <admin_token>
```
Period options: week, month, year

## Database Models

### User
- firstName, lastName
- email (unique)
- password (hashed)
- mobilePhone
- profilePicture
- role (customer, seller, admin)
- isActive
- activation/reset tokens

### Product
- title, description
- price, category
- images array
- seller (reference to User)
- stock
- rating, numReviews
- reviews array
- isFeatured, isActive

### Cart
- user (reference to User)
- items array (product, quantity, price)
- totalPrice

### Order
- user (reference to User)
- items array
- shippingAddress
- paymentMethod, paymentResult
- totalPrice
- status (pending, processing, shipped, delivered, cancelled)
- isPaid, isDelivered

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with salt rounds
- **Helmet**: Security headers
- **Rate Limiting**: Prevent abuse (100 requests per 15 minutes)
- **CORS**: Configured for frontend origin
- **Input Validation**: Server-side validation
- **Role-Based Access Control**: Admin, Seller, Customer roles

## Error Handling

All endpoints return consistent error responses:

```json
{
  "message": "Error description"
}
```

HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Testing the API

You can test the API using:
- **Postman**: Import the endpoints
- **cURL**: Command line testing
- **Frontend Integration**: Connect your React app

### Example cURL Request
```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "password": "password123",
    "confirmPassword": "password123",
    "mobilePhone": "+1234567890"
  }'
```

## Support

For issues or questions, please refer to the project repository.
