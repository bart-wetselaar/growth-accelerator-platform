# Custom Domain Configuration for Growth Accelerator Platform
# Domain: app.growthaccelerator.nl
# Azure Web App: ga-hwaffmb0eqajfza5

## Configuration Summary

**Primary Custom Domain**: app.growthaccelerator.nl
**Azure Web App**: ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net
**Deployment Method**: GitHub Actions → Azure Web App with custom domain binding

## DNS Configuration Required

To complete the custom domain setup, ensure these DNS records are configured:

```
Type: CNAME
Name: app (or @)
Value: ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net
TTL: 3600
```

## SSL Certificate

Azure Web App will automatically provision an SSL certificate for app.growthaccelerator.nl once:
1. DNS is correctly configured
2. Domain verification is completed in Azure portal
3. Custom domain is added to the Azure Web App

## Verification Steps

1. DNS propagation: `nslookup app.growthaccelerator.nl`
2. Azure domain verification: Azure portal → Web App → Custom domains
3. SSL certificate status: Azure portal → Web App → TLS/SSL settings
4. Health check: `curl https://app.growthaccelerator.nl/health`

## Deployment Process

1. Code changes pushed to GitHub
2. GitHub Actions workflow triggered
3. Application deployed to Azure Web App
4. Both URLs serve the same application:
   - https://app.growthaccelerator.nl
   - https://ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net

Generated: 2025-06-26T17:26:19.300637
