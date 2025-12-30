#!/bin/bash
# Server Setup Script for Automation Control System
# Run this once on your deployment server to prepare it

set -e

DEPLOY_PATH="/home/a_krasichenok/automation-control-system"

echo "=============================================="
echo "Automation Control System - Server Setup"
echo "=============================================="

# Check if running as correct user
if [ "$(whoami)" != "a_krasichenok" ]; then
    echo "Please run as a_krasichenok user"
    exit 1
fi

# Create deployment directory
echo "Creating deployment directory..."
mkdir -p "$DEPLOY_PATH"
mkdir -p "$DEPLOY_PATH/scripts"

# Check Docker installation
echo "Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first:"
    echo "  curl -fsSL https://get.docker.com | sh"
    echo "  sudo usermod -aG docker \$USER"
    exit 1
fi

# Check Docker Compose
echo "Checking Docker Compose..."
if ! docker compose version &> /dev/null; then
    echo "Docker Compose plugin not found. Please install it:"
    echo "  sudo apt install docker-compose-plugin"
    exit 1
fi

# Create .env file if not exists
if [ ! -f "$DEPLOY_PATH/.env" ]; then
    echo "Creating .env file..."
    cat > "$DEPLOY_PATH/.env" << 'EOF'
# Production Environment - Configure these values!
SECRET_KEY=CHANGE_ME_TO_A_32_CHAR_SECRET_KEY
API_KEY=CHANGE_ME_TO_YOUR_API_KEY
API_KEY_REQUIRED=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
CORS_ORIGINS=*
PORT=5000
EOF
    echo ""
    echo "⚠️  IMPORTANT: Edit $DEPLOY_PATH/.env and set your secret keys!"
    echo ""
fi

# Set permissions
chmod 600 "$DEPLOY_PATH/.env"

echo ""
echo "=============================================="
echo "Server setup complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Edit $DEPLOY_PATH/.env with your production secrets"
echo "2. Set up GitHub Secrets for deployment:"
echo "   - SSH_PRIVATE_KEY: Your SSH private key"
echo "3. Push to main/master branch to trigger deployment"
echo ""

