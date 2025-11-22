# Render Deployment Guide for Math Solver Pro

## Prerequisites
- A Render account (https://render.com)
- GitHub repository with your code

## Deployment Steps

### 1. Push Code to GitHub
```bash
git push origin deploy/render
```

### 2. Create New Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `ecuaciones` repository
5. Configure the service:

#### Basic Settings
- **Name**: `ecuaciones` (or your preferred name)
- **Region**: Select closest to your users (e.g., Virginia if US East)
- **Branch**: `deploy/render`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

#### Build & Deploy
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn math_project.wsgi:application`

### 3. Environment Variables

Add these environment variables in Render dashboard:

| Variable Name | Value | Notes |
|--------------|-------|-------|
| `SECRET_KEY` | (Click "Generate") | Auto-generate a secure key |
| `DEBUG` | `False` | Production setting |
| `ALLOWED_HOSTS` | (leave empty) | Will auto-configure |
| `PYTHON_VERSION` | `3.11.0` | Python version |

**Note**: Render automatically adds:
- `DATABASE_URL` (if you add a PostgreSQL database)
- `RENDER=True`
- `RENDER_EXTERNAL_HOSTNAME`

### 4. Add PostgreSQL Database (Optional)

If you want to use PostgreSQL instead of SQLite:

1. From your service dashboard, click "New" → "PostgreSQL"
2. Name it (e.g., `ecuaciones-db`)
3. Select the Free tier
4. Click "Create Database"
5. Go back to your web service
6. In "Environment" tab, click "Add Environment Variable"
7. Select "Add from Database" → Choose your PostgreSQL database
8. It will automatically add `DATABASE_URL`

### 5. Deploy

1. Click "Create Web Service" or "Manual Deploy" → "Deploy latest commit"
2. Wait for build to complete (5-10 minutes)
3. Your app will be available at `https://your-service-name.onrender.com`

## Using render.yaml (Alternative)

You can also use the included `render.yaml` file for infrastructure-as-code deployment:

1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your repository
3. Select branch `deploy/render`
4. Render will automatically detect `render.yaml`
5. Click "Apply"

## Post-Deployment

### Access Your Site
Visit: `https://your-service-name.onrender.com/solver/`

### Check Logs
- In Render dashboard → Your service → "Logs" tab
- View real-time logs and errors

### Manual Deploy
If auto-deploy is disabled:
- Go to "Manual Deploy" → "Deploy latest commit"

## Troubleshooting

### Static Files Not Loading
1. Check build logs for "collectstatic" success
2. Verify `STATIC_ROOT` in settings.py
3. Ensure WhiteNoise is in MIDDLEWARE

### Database Errors
1. Ensure migrations ran successfully in build logs
2. Check `DATABASE_URL` is set (if using PostgreSQL)
3. Run manual migration: `python manage.py migrate`

### Application Errors
1. Check logs for detailed error messages
2. Verify all environment variables are set
3. Ensure `DEBUG=False` in production

### 500 Errors
1. Check `ALLOWED_HOSTS` includes your Render domain
2. Verify `SECRET_KEY` is set
3. Review application logs for stack traces

## Free Tier Limitations

Render Free tier includes:
- 512 MB RAM
- Service spins down after 15 minutes of inactivity
- First request after spin-down will be slow (30-60 seconds)
- Shared CPU

For production use, consider upgrading to Starter ($7/month) or higher tiers.

## Updating Your Deployment

1. Make changes locally
2. Commit and push to `deploy/render` branch:
   ```bash
   git add .
   git commit -m "Update: description"
   git push origin deploy/render
   ```
3. Render will auto-deploy if enabled, or click "Manual Deploy"

## Environment Variables Reference

### Required
- `SECRET_KEY`: Django secret key (auto-generated)
- `DEBUG`: Set to `False` for production

### Optional
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: PostgreSQL connection string (auto-set by Render)
- `WEB_CONCURRENCY`: Number of Gunicorn workers (default: 4)

## Security Checklist

✅ DEBUG=False in production
✅ SECRET_KEY is unique and secret
✅ ALLOWED_HOSTS is properly configured
✅ HTTPS enforced (automatic on Render)
✅ Static files served via WhiteNoise
✅ Database uses PostgreSQL (recommended)

## Support

- Render Documentation: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Project Issues: https://github.com/JoaquiinAguilar/Ecuaciones/issues
