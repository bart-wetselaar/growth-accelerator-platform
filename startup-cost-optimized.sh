#!/bin/bash
# Cost-Optimized Azure Web App Startup for Growth Accelerator Platform
# Reduces resource usage and optimizes PM2 configuration

echo "Starting Growth Accelerator Platform with cost optimizations..."

# Set environment variables for cost optimization
export NODE_ENV=production
export PM2_CONCURRENT_ACTIONS=1
export PM2_KILL_TIMEOUT=5000
export PM2_GRACEFUL_TIMEOUT=3000

# Install PM2 with minimal footprint
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2 with minimal configuration..."
    npm install -g pm2@latest --production --no-optional
fi

# Create optimized dist directory
mkdir -p /home/site/wwwroot/dist

# Copy only essential files to reduce storage costs
if [ -f "index.html" ]; then
    # Minify HTML on-the-fly to reduce bandwidth costs
    sed 's/>[[:space:]]*</></g' index.html > /home/site/wwwroot/dist/index.html
fi

# Copy and optimize static assets
if [ -d "static" ]; then
    # Copy only essential static files
    find static -name "*.css" -o -name "*.js" -o -name "*.png" -o -name "*.jpg" -o -name "*.svg" |     while read file; do
        cp "$file" "/home/site/wwwroot/dist/" 2>/dev/null || true
    done
fi

# Create optimized PM2 ecosystem file for cost efficiency
cat > /home/site/wwwroot/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'growth-accelerator-static',
    script: 'serve',
    args: '/home/site/wwwroot/dist --no-daemon --single',
    instances: 1,
    exec_mode: 'fork',
    max_memory_restart: '100M',
    env: {
      NODE_ENV: 'production',
      PORT: process.env.PORT || 8080
    },
    log_file: '/home/LogFiles/pm2.log',
    error_file: '/home/LogFiles/pm2-error.log',
    out_file: '/home/LogFiles/pm2-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    merge_logs: true,
    max_restarts: 3,
    min_uptime: '5s',
    kill_timeout: 3000,
    listen_timeout: 8000,
    shutdown_with_message: true,
    wait_ready: true
  }]
};
EOF

echo "Contents of optimized dist directory:"
ls -la /home/site/wwwroot/dist/

# Start PM2 with cost-optimized configuration
echo "Starting PM2 with cost optimizations..."
cd /home/site/wwwroot
pm2 start ecosystem.config.js --no-daemon

# Fallback to simple serve if ecosystem fails
if [ $? -ne 0 ]; then
    echo "Fallback: Starting simple PM2 serve..."
    pm2 serve /home/site/wwwroot/dist --no-daemon --port ${PORT:-8080}
fi
