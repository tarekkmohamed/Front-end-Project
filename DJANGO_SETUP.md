# Django Backend Setup Guide

This guide will help you set up and run the Django E-commerce backend.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- SQLite (included with Python) or PostgreSQL
- Git

## Quick Start

### 1. Navigate to Django Backend Directory
```bash
cd django_backend
```

### 2. Create and Activate Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit the `.env` file with your settings. For development, the defaults work fine:
```env
SECRET_KEY=<your-secret-key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
FRONTEND_URL=http://localhost:5173
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Seed Database with Sample Data
```bash
python manage.py seed_db
```

This creates:
- **Admin**: admin@ecommerce.com / admin123
- **Seller**: seller@ecommerce.com / seller123
- **Customer**: customer@ecommerce.com / customer123
- Sample products, categories, brands, and tags

### 7. Create Superuser (Optional, if not using seed)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The server will be available at: **http://localhost:8000**

## Accessing the Application

### API Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### Django Admin Panel
- **URL**: http://localhost:8000/admin/
- **Login**: Use admin credentials (admin@ecommerce.com / admin123)

### API Base URL
- **Development**: http://localhost:8000/api/

## API Endpoints Overview

### Authentication
- `POST /api/auth/register/` - Register new user
- `GET /api/auth/activate/<token>/` - Activate account
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Get/Update profile

### Products
- `GET /api/products/` - List products
- `GET /api/products/<id>/` - Product details
- `POST /api/products/create/` - Create product (Seller/Admin)
- `GET /api/products/featured/` - Featured products

### Cart
- `GET /api/cart/` - Get cart
- `POST /api/cart/add/` - Add to cart
- `PUT /api/cart/items/<id>/update/` - Update quantity
- `DELETE /api/cart/items/<id>/remove/` - Remove item

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/create/` - Create order
- `GET /api/orders/<id>/` - Order details

## Testing the API

### Example: Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ecommerce.com",
    "password": "admin123"
  }'
```

### Example: Get Products
```bash
curl http://localhost:8000/api/products/
```

### Example: Get Product Detail
```bash
curl http://localhost:8000/api/products/1/
```

### Example: Authenticated Request
```bash
# First, login to get the access token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"admin123"}' | jq -r '.tokens.access')

# Then use the token for authenticated requests
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

## PostgreSQL Setup (Production)

### 1. Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

### 2. Create Database
```bash
sudo -u postgres psql
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### 3. Update .env
```env
DATABASE_URL=postgresql://ecommerce_user:your_password@localhost:5432/ecommerce_db
```

### 4. Run Migrations
```bash
python manage.py migrate
```

## Email Configuration

For email functionality (activation, password reset), configure email settings in `.env`:

### Gmail Setup
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@ecommerce.com
```

**Note**: For Gmail, you need to generate an App Password:
1. Go to Google Account settings
2. Security → 2-Step Verification
3. App passwords → Generate new password
4. Use the generated password in `EMAIL_HOST_PASSWORD`

## Production Deployment

### 1. Update Environment Variables
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=<generate-strong-secret-key>
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 2. Collect Static Files
```bash
python manage.py collectstatic
```

### 3. Install Gunicorn
```bash
pip install gunicorn
```

### 4. Run with Gunicorn
```bash
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:8000
```

### 5. Configure Nginx (Optional)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

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

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Migration Issues
```bash
# Reset migrations (CAUTION: This deletes data)
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

## Common Commands

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Seed database
python manage.py seed_db

# Shell access
python manage.py shell

# Check for issues
python manage.py check
```

## Development Tips

### Enable Debug Toolbar (Optional)
```bash
pip install django-debug-toolbar
```

Add to `INSTALLED_APPS` in settings.py:
```python
'debug_toolbar',
```

### Run Server on Different Port
```bash
python manage.py runserver 8080
```

### Access from Other Devices
```bash
python manage.py runserver 0.0.0.0:8000
```

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use PostgreSQL in production
- [ ] Enable HTTPS/SSL
- [ ] Configure email backend properly
- [ ] Set up proper CORS settings
- [ ] Regular security updates
- [ ] Use environment variables for sensitive data

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Support

For issues or questions:
1. Check the API documentation at `/api/docs/`
2. Review Django logs for errors
3. Check the README.md for more details

---

Happy Coding! 🚀
