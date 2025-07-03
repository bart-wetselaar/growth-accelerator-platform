#!/bin/bash
# Azure Web App startup script with PM2 for web
# Updated based on user configuration: pm2 serve /home/site/wwwroot/dist --no-daemon

echo "Starting Growth Accelerator Platform with PM2"
echo "Azure Web App: ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net"
echo "Custom Domain: web"

# Set environment variables
export AZURE_WEBAPP_NAME=ga-hwaffmb0eqajfza5
export CUSTOM_DOMAIN=web
export FLASK_ENV=production

# Install PM2 globally
npm install -g pm2

# Create dist directory and copy static files
mkdir -p /home/site/wwwroot/dist

# Copy static files to dist directory
if [ -f "templates/index.html" ]; then
    cp templates/index.html /home/site/wwwroot/dist/
fi

if [ -d "static" ]; then
    cp -r static /home/site/wwwroot/dist/
fi

# Create a simple index.html if not exists
if [ ! -f "/home/site/wwwroot/dist/index.html" ]; then
    cat > /home/site/wwwroot/dist/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Accelerator Platform</title>
    <style>
        body { font-family: Arial, sans-serif; background: #00205b; color: white; text-align: center; padding: 50px; }
        h1 { font-size: 3em; margin-bottom: 20px; }
        .status { background: #10b981; padding: 10px 20px; border-radius: 20px; display: inline-block; }
    </style>
</head>
<body>
    <h1>Growth Accelerator Platform</h1>
    <div class="status">✓ Azure Web App Online with PM2</div>
    <p>Served by PM2 on web</p>
</body>
</html>
EOF
fi

# Start PM2 server as specified in Azure configuration
echo "Starting PM2 server..."
pm2 serve /home/site/wwwroot/dist --no-daemon --port 8000 --name "growth-accelerator"
