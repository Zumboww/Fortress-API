#!/bin/bash

# Fortress API Setup Script
# This script sets up the development environment

echo "🏰 Setting up Fortress API..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install dev dependencies
read -p "Install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -r requirements-dev.txt
fi

# Create .env file from example
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration!"
fi

# Create users.csv from sample if doesn't exist
if [ ! -f users.csv ]; then
    echo ""
    echo "👥 Creating users.csv from sample..."
    cp users.sample.csv users.csv
    echo "⚠️  Please update users.csv with hashed passwords!"
    echo ""
    echo "To generate hashed passwords, run:"
    echo "python3 -c \"from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['argon2'], deprecated='auto'); print(pwd_context.hash('your_password'))\""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate  # Linux/Mac"
echo "   venv\\Scripts\\activate     # Windows"
echo ""
echo "2. Update .env with your configuration"
echo ""
echo "3. Update users.csv with hashed passwords"
echo ""
echo "4. Run the server:"
echo "   uvicorn system:sapp --reload"
echo ""
echo "5. Visit http://localhost:8000/docs"
echo ""
echo "🎉 Happy coding!"
