#!/bin/bash
# Azure Web App startup script for Growth Accelerator Platform
# Uses PM2 to serve static files as configured in Azure portal

echo "Starting Growth Accelerator Platform with PM2..."
echo "Working directory: $(pwd)"
echo "Contents:"
ls -la

# Install PM2 globally if not present
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2..."
    npm install -g pm2
fi

# Ensure dist directory exists
mkdir -p /home/site/wwwroot/dist

# Copy files to dist if they exist
if [ -f "index.html" ]; then
    cp index.html /home/site/wwwroot/dist/
fi

if [ -d "static" ]; then
    cp -r static/* /home/site/wwwroot/dist/ 2>/dev/null || true
fi

if [ -d "templates" ]; then
    cp -r templates/* /home/site/wwwroot/dist/ 2>/dev/null || true
fi

# Create default index.html if none exists
if [ ! -f "/home/site/wwwroot/dist/index.html" ]; then
    cat > /home/site/wwwroot/dist/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Accelerator Platform</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #00205b 0%, #1e40af 100%); min-height: 100vh; color: white; display: flex; align-items: center; justify-content: center; margin: 0; }
        .container { text-align: center; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 20px; padding: 40px; }
        .btn { background: linear-gradient(135deg, #ff5571, #ef4444); border: none; border-radius: 50px; padding: 15px 30px; color: white; text-decoration: none; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Growth Accelerator Platform</h1>
        <p>Match. Onboard. Hire.</p>
        <div style="background: #28a745; color: white; padding: 8px 16px; border-radius: 20px; display: inline-block; margin: 20px 0;">Azure Web App Active</div>
        <br><br>
        <a href="/api/health" class="btn">Health Check</a>
    </div>
</body>
</html>
EOF
fi

echo "Contents of dist directory:"
ls -la /home/site/wwwroot/dist/

# Start PM2 with the exact command from Azure portal
echo "Starting PM2 with command: pm2 serve /home/site/wwwroot/dist --no-daemon"
pm2 serve /home/site/wwwroot/dist --no-daemon
