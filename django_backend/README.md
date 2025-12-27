# Django E-commerce Backend API

A comprehensive, secure, and scalable E-commerce backend built with Django and Django REST Framework.

## 🚀 Features

### Authentication System
- User registration with email validation
- Account activation via email (24-hour validity)
- JWT-based authentication
- Password reset functionality
- User profile management
- Role-based access control (Customer, Seller, Admin)

### Product Management
- Full CRUD operations for products
- Product categories, tags, and brands
- Multiple product images support
- Product search and filtering
- Featured products
- Product reviews and ratings
- Seller product management

### Shopping Cart
- Persistent cart for authenticated users
- Add, update, remove items
- Stock validation
- Cart total calculation

### Order Management
- Order creation from cart
- Multiple shipping addresses
- Order status tracking
- Order history
- Payment simulation
- Email notifications

### Admin Panel
- Django Admin interface for all models
- Custom admin actions
- Product moderation
- User management
- Order management

## 📋 Requirements

- Python 3.8+
- Django 5.0
- PostgreSQL (production) / SQLite (development)
- See `requirements.txt` for full dependencies

## 🔧 Installation

### 1. Clone the repository
```bash
cd django_backend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Email settings (for activation and password reset)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Seed database (Optional)
```bash
python manage.py seed_db
```

This creates:
- Admin user: admin@ecommerce.com / admin123
- Seller user: seller@ecommerce.com / seller123
- Customer user: customer@ecommerce.com / customer123
- Sample categories, brands, tags, and products

### 7. Create superuser (if not using seed)
```bash
python manage.py createsuperuser
```

### 8. Run development server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### API Endpoints

#### Authentication (`/api/auth/`)
- `POST /api/auth/register/` - Register new user
- `GET /api/auth/activate/<token>/` - Activate account
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/<token>/` - Reset password
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password

#### Products (`/api/products/`)
- `GET /api/products/` - List products (with filtering)
- `GET /api/products/<id>/` - Product details
- `POST /api/products/create/` - Create product (Seller/Admin)
- `PUT /api/products/<id>/update/` - Update product (Owner/Admin)
- `DELETE /api/products/<id>/delete/` - Delete product (Owner/Admin)
- `GET /api/products/featured/` - Featured products
- `GET /api/products/latest/` - Latest products
- `GET /api/products/seller/my-products/` - Seller's products
- `POST /api/products/<id>/upload-image/` - Upload product image
- `GET /api/products/categories/` - List categories
- `GET /api/products/tags/` - List tags
- `GET /api/products/brands/` - List brands

#### Reviews (`/api/`)
- `GET /api/products/<id>/reviews/` - List product reviews
- `POST /api/products/<id>/reviews/create/` - Add review

#### Cart (`/api/cart/`)
- `GET /api/cart/` - Get cart
- `POST /api/cart/add/` - Add to cart
- `PUT /api/cart/items/<id>/update/` - Update cart item
- `DELETE /api/cart/items/<id>/remove/` - Remove cart item
- `DELETE /api/cart/clear/` - Clear cart

#### Orders (`/api/orders/`)
- `GET /api/orders/` - List user orders
- `POST /api/orders/create/` - Create order
- `GET /api/orders/<id>/` - Order details
- `POST /api/orders/<id>/pay/` - Mark as paid
- `GET /api/orders/shipping-addresses/` - List shipping addresses
- `POST /api/orders/shipping-addresses/` - Create shipping address
- `GET /api/orders/shipping-addresses/<id>/` - Shipping address details
- `PUT /api/orders/shipping-addresses/<id>/` - Update shipping address
- `DELETE /api/orders/shipping-addresses/<id>/` - Delete shipping address

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Example Login Request:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@ecommerce.com",
    "password": "customer123"
  }'
```

### Example Authenticated Request:
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer <your_access_token>"
```

## 🗄️ Database Models

### User Model
- Custom user model extending AbstractUser
- Email as username field
- Roles: customer, seller, admin
- Activation and password reset tokens

### UserProfile Model
- OneToOne relationship with User
- Address, birthdate, city, country

### Product Model
- Title, description, price, stock
- Category, tags, brand relationships
- Seller reference
- Approval and featured flags
- Average rating and review count

### ProductImage Model
- Multiple images per product
- Primary image flag

### Category, Tag, Brand Models
- Organizational models for products

### Review Model
- Product reviews with ratings (1-5)
- One review per user per product

### Cart & CartItem Models
- User-specific carts
- Product quantity tracking

### Order & OrderItem Models
- Order with shipping details
- Order status tracking
- Payment tracking
- Product snapshot at order time

### ShippingAddress Model
- Multiple addresses per user
- Default address flag

## 🛡️ Security Features

- JWT authentication with token refresh
- Password hashing with Django's built-in system
- Email verification for account activation
- CORS configuration for frontend
- Role-based permissions
- Input validation with Django REST Framework serializers
- Protection against common web vulnerabilities

## 🚀 Production Deployment

### 1. Update settings for production
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce
SECRET_KEY=your-strong-secret-key
```

### 2. Configure PostgreSQL
```bash
# Install psycopg2
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 3. Collect static files
```bash
python manage.py collectstatic
```

### 4. Run with Gunicorn
```bash
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:8000
```

### 5. Set up Nginx as reverse proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

## 📊 Database Schema

```
User (users_user)
├── UserProfile (users_userprofile)
├── Product (products_product) [seller]
├── Review (reviews_review) [user]
├── Cart (cart_cart) [user]
├── Order (orders_order) [user]
└── ShippingAddress (orders_shippingaddress) [user]

Product
├── Category (products_category)
├── Brand (products_brand)
├── Tag (products_tag) [many-to-many]
├── ProductImage (products_productimage)
├── Review (reviews_review) [product]
└── CartItem (cart_cartitem) [product]

Cart
└── CartItem (cart_cartitem)

Order
└── OrderItem (orders_orderitem)
```

## 🧪 Testing

Run Django tests:
```bash
python manage.py test
```

## 📝 Development

### Code Style
The project follows Django best practices and PEP 8 style guide.

### Adding New Features
1. Create models in `models.py`
2. Create serializers in `serializers.py`
3. Create views in `views.py`
4. Add URL patterns in `urls.py`
5. Register in admin (optional)
6. Create migrations: `python manage.py makemigrations`
7. Apply migrations: `python manage.py migrate`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
- Check the API documentation at `/api/docs/`
- Review the Django logs
- Open an issue on GitHub

## 📞 Contact

For more information, contact: admin@ecommerce.com

---

Built with ❤️ using Django and Django REST Framework
