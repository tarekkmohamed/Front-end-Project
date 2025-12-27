# Quick Start Guide

Get the E-commerce application up and running in minutes!

## Prerequisites

Before you begin, ensure you have:
- Node.js (v14 or higher) installed
- MongoDB (v4.4 or higher) installed and running
- npm or yarn package manager

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Front-end-Project
```

## Step 2: Backend Setup

### Install Dependencies
```bash
cd backend
npm install
```

### Configure Environment
```bash
cp .env.example .env
```

Edit `backend/.env` and update these critical values:
- `JWT_SECRET` - Change to a secure random string
- `MONGODB_URI` - Update if not using local MongoDB
- Email settings (optional, for activation emails)

### Start MongoDB
Open a new terminal and start MongoDB:
```bash
mongod
```

### Seed the Database (Optional)
Populate the database with test data:
```bash
npm run seed
```

This creates test accounts:
- **Admin**: admin@ecommerce.com / admin123
- **Seller**: seller@ecommerce.com / seller123  
- **Customer**: customer@ecommerce.com / customer123

### Start Backend Server
```bash
npm run dev
```

The backend will run on http://localhost:5000

## Step 3: Frontend Setup

### Install Dependencies
Open a new terminal in the project root:
```bash
npm install
```

### Start Frontend
```bash
npm run dev
```

The frontend will run on http://localhost:5173

## Step 4: Test the Application

1. Open http://localhost:5173 in your browser
2. Browse products (uses fake API initially)
3. Try login with test accounts (after backend integration)

## Next Steps

### For Development
1. Read `INTEGRATION_GUIDE.md` to connect frontend with backend
2. Review `backend/README.md` for API documentation
3. Explore the codebase structure

### Testing Backend API
Use these test credentials to test backend endpoints:

**Admin Access**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"admin123"}'
```

**Get Products**:
```bash
curl http://localhost:5000/api/products
```

**Health Check**:
```bash
curl http://localhost:5000/api/health
```

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongod`
- Check MONGODB_URI in backend/.env
- Verify MongoDB service status

### Port Already in Use
- Backend (5000): Kill process or change PORT in .env
- Frontend (5173): Vite will automatically try another port

### Module Not Found Errors
```bash
# Backend
cd backend && npm install

# Frontend  
cd .. && npm install
```

### Cannot Login
- Ensure backend is running on port 5000
- Check browser console for errors
- Verify MongoDB is running and seeded

## Project Structure

```
Front-end-Project/
├── backend/           # Node.js/Express API
│   ├── controllers/   # Request handlers
│   ├── models/        # Database schemas
│   ├── routes/        # API routes
│   └── server.js      # Entry point
├── src/               # React frontend
│   ├── components/    # Reusable components
│   ├── screens/       # Page components
│   └── App.jsx        # Main app
└── README.md          # Main documentation
```

## Available Scripts

### Backend
- `npm start` - Start production server
- `npm run dev` - Start with auto-reload
- `npm run seed` - Seed database with test data

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint

## Support & Documentation

- **API Docs**: `backend/README.md`
- **Integration Guide**: `INTEGRATION_GUIDE.md`
- **Main README**: `README.md`

## Common Tasks

### Create a New Admin User
```javascript
// Using MongoDB shell or Compass
db.users.updateOne(
  { email: "user@example.com" },
  { $set: { role: "admin" } }
)
```

### Reset Database
```bash
cd backend
npm run seed
```

### View API Health
Navigate to: http://localhost:5000/api/health

## Production Deployment

### Backend
1. Set `NODE_ENV=production` in environment
2. Update MongoDB URI to production database
3. Configure email service credentials
4. Deploy to your hosting platform

### Frontend
1. Update API URL in environment variables
2. Build: `npm run build`
3. Deploy `dist` folder to hosting service

---

🎉 **You're all set!** Start building your E-commerce features.

For detailed information, see:
- [Complete README](README.md)
- [Backend API Documentation](backend/README.md)
- [Integration Guide](INTEGRATION_GUIDE.md)
