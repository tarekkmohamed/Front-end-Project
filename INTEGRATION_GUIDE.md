# Frontend Integration Guide

This guide will help you integrate the backend API with the existing React frontend.

## Overview

The backend API is now available at `http://localhost:5000/api`. You need to update the frontend to use these endpoints instead of the fake API.

## Changes Needed in Frontend

### 1. Update API Base URL

Create a new file `src/config/api.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add token to requests if available
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Handle response errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Clear token and redirect to login
            localStorage.removeItem('token');
            window.location.href = '/login-page';
        }
        return Promise.reject(error);
    }
);

export default api;
```

### 2. Update Home Screen (Product Listing)

Update `src/screens/Home.jsx`:

```javascript
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from '../components/ProductCard/ProductCard';
import api from '../config/api';

const Home = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [category, setCategory] = useState('');

    useEffect(() => {
        fetchProducts();
    }, [searchTerm, category]);

    const fetchProducts = async () => {
        try {
            setLoading(true);
            const params = {};
            if (searchTerm) params.search = searchTerm;
            if (category) params.category = category;
            
            const res = await api.get('/products', { params });
            setProducts(res.data.products);
            setError(null);
        } catch (error) {
            console.error(error);
            setError('Failed to load products');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='home-container'>
            <h1>Our Products</h1>
            
            {/* Add filters */}
            <div className="filters">
                <input 
                    type="text" 
                    placeholder="Search products..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <select value={category} onChange={(e) => setCategory(e.target.value)}>
                    <option value="">All Categories</option>
                    <option value="electronics">Electronics</option>
                    <option value="clothing">Clothing</option>
                    <option value="books">Books</option>
                    <option value="home">Home</option>
                    <option value="sports">Sports</option>
                </select>
            </div>

            {loading && <p>Loading...</p>}
            {error && <p className="error">{error}</p>}
            
            <div className="products-container">
                {products.map((item) => (
                    <ProductCard product={item} key={item._id}></ProductCard>
                ))}
            </div>
        </div>
    );
};

export default Home;
```

### 3. Update Login Screen

Update `src/screens/Login.jsx`:

```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { login } from '../store/Slices/userSlice';
import api from '../config/api';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import './Login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handleLogin = async (ev) => {
        ev.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await api.post('/auth/login', {
                email,
                password
            });

            // Save token
            localStorage.setItem('token', response.data.token);
            
            // Update Redux store
            dispatch(login(response.data.user));
            
            // Navigate to profile
            navigate('/Profile-Page');
        } catch (error) {
            console.error(error);
            setError(error.response?.data?.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='background'>
            <div className='login-layout'>
                <h1>Login</h1>
                {error && <p className="error-message">{error}</p>}
                
                <form onSubmit={handleLogin}>
                    <div className='input-container'>
                        <TextField
                            required
                            label="Email"
                            variant="standard"
                            type='email'
                            value={email}
                            onChange={ev => setEmail(ev.target.value)}
                        />
                        <TextField
                            required
                            label="Password"
                            type="password"
                            autoComplete="current-password"
                            variant="standard"
                            value={password}
                            onChange={ev => setPassword(ev.target.value)}
                        />
                    </div>
                    
                    <div className='checkbox-container'>
                        <div>
                            <Checkbox id='checkbox' />
                            <label htmlFor="checkbox">Remember Me</label>
                        </div>
                        <p>Forgot Password?</p>
                    </div>
                    
                    <div className='custom-btn'>
                        <button type='submit' disabled={loading}>
                            {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
```

### 4. Create Registration Screen

Create `src/screens/Register.jsx`:

```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../config/api';
import TextField from '@mui/material/TextField';

const Register = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        mobilePhone: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            const response = await api.post('/auth/register', formData);
            setSuccess(response.data.message);
            
            // Redirect to login after 2 seconds
            setTimeout(() => {
                navigate('/login-page');
            }, 2000);
        } catch (error) {
            console.error(error);
            setError(error.response?.data?.message || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='background'>
            <div className='login-layout'>
                <h1>Register</h1>
                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}
                
                <form onSubmit={handleSubmit}>
                    <TextField
                        required
                        name="firstName"
                        label="First Name"
                        variant="standard"
                        value={formData.firstName}
                        onChange={handleChange}
                    />
                    <TextField
                        required
                        name="lastName"
                        label="Last Name"
                        variant="standard"
                        value={formData.lastName}
                        onChange={handleChange}
                    />
                    <TextField
                        required
                        name="email"
                        label="Email"
                        type="email"
                        variant="standard"
                        value={formData.email}
                        onChange={handleChange}
                    />
                    <TextField
                        required
                        name="mobilePhone"
                        label="Mobile Phone"
                        variant="standard"
                        value={formData.mobilePhone}
                        onChange={handleChange}
                    />
                    <TextField
                        required
                        name="password"
                        label="Password"
                        type="password"
                        variant="standard"
                        value={formData.password}
                        onChange={handleChange}
                    />
                    <TextField
                        required
                        name="confirmPassword"
                        label="Confirm Password"
                        type="password"
                        variant="standard"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                    />
                    
                    <button type='submit' disabled={loading}>
                        {loading ? 'Registering...' : 'Register'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Register;
```

### 5. Update Cart Context

Update `src/components/CartContext.jsx` to sync with backend:

```javascript
import React, { createContext, useState, useEffect } from 'react';
import api from '../config/api';

export const CartContext = createContext();

export function CartProvider({ children }) {
    const [cart, setCart] = useState([]);
    const [loading, setLoading] = useState(false);

    // Load cart from backend on mount
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            loadCart();
        }
    }, []);

    const loadCart = async () => {
        try {
            const response = await api.get('/cart');
            setCart(response.data.items || []);
        } catch (error) {
            console.error('Failed to load cart:', error);
        }
    };

    const addToCart = async (product) => {
        try {
            setLoading(true);
            await api.post('/cart', {
                productId: product._id || product.id,
                quantity: 1
            });
            await loadCart(); // Reload cart
            window.alert('Product added to cart!');
        } catch (error) {
            console.error(error);
            window.alert(error.response?.data?.message || 'Failed to add to cart');
        } finally {
            setLoading(false);
        }
    };

    const removeFromCart = async (itemId) => {
        try {
            setLoading(true);
            await api.delete(`/cart/${itemId}`);
            await loadCart(); // Reload cart
        } catch (error) {
            console.error('Failed to remove from cart:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <CartContext.Provider value={{ cart, addToCart, removeFromCart, loading }}>
            {children}
        </CartContext.Provider>
    );
}
```

### 6. Add Registration Route

Update `src/App.jsx` to include the registration route:

```javascript
import Register from './screens/Register';

function App() {
    return (
        <>
            <Navbar></Navbar>
            <Routes>
                <Route path='/' Component={Home}></Route>
                <Route path='/product/:id' Component={ProductDetails}></Route>
                <Route path='/cart' Component={Cart}></Route>
                <Route path='/login-page' Component={Login}></Route>
                <Route path='/register' Component={Register}></Route>
                <Route path='/Profile-Page' Component={userDetails}></Route>
            </Routes>
        </>
    );
}
```

### 7. Environment Variables

Create `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5000/api
```

## Testing Integration

1. **Start Backend Server**:
```bash
cd backend
npm run dev
```

2. **Start Frontend**:
```bash
# From root directory
npm run dev
```

3. **Test Features**:
   - Register a new account
   - Check email for activation (if email is configured)
   - Login with credentials
   - Browse products
   - Add items to cart
   - Create an order

## Important Notes

- Make sure MongoDB is running before starting the backend
- Update the `.env` files with correct configuration
- For production, update CORS settings in backend to match your frontend domain
- Configure email service for activation and notifications to work

## API Endpoints Reference

See `backend/README.md` for complete API documentation.

## Troubleshooting

### CORS Errors
- Ensure backend CORS is configured for `http://localhost:5173`
- Check that `FRONTEND_URL` in backend `.env` matches your frontend URL

### Authentication Errors
- Check that JWT_SECRET is set in backend `.env`
- Verify token is being saved to localStorage
- Check browser console for detailed error messages

### Database Connection Errors
- Ensure MongoDB is running
- Verify MONGODB_URI in backend `.env`
- Check MongoDB logs for connection issues
