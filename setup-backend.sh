#!/bin/bash

# E-commerce Backend Setup Script

echo "=========================================="
echo "E-commerce Backend Setup"
echo "=========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✓ Node.js version: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✓ npm version: $(npm --version)"

# Check if MongoDB is installed
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB is not installed or not in PATH."
    echo "   Please install MongoDB from https://www.mongodb.com/try/download/community"
else
    echo "✓ MongoDB is installed"
fi

echo ""
echo "Installing backend dependencies..."
cd backend
npm install

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "Setting up environment configuration..."

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and configure:"
    echo "   - MongoDB connection string (MONGODB_URI)"
    echo "   - JWT secret key (JWT_SECRET)"
    echo "   - Email settings (EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure MongoDB is running (start with 'mongod' command)"
echo "2. Edit backend/.env with your configuration"
echo "3. Start the backend server:"
echo "   cd backend"
echo "   npm run dev     # Development mode with auto-reload"
echo "   npm start       # Production mode"
echo ""
echo "The server will run on http://localhost:5000"
echo "API documentation: backend/README.md"
echo ""
