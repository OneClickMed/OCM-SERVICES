# Setup Checklist

Use this checklist to ensure your OCM Service Backend is properly configured.

## ✅ Initial Setup

- [ ] Python 3.9+ installed
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example`
- [ ] Database migrations run (`python manage.py migrate`)

## ✅ Environment Variables

### Required for Basic Operation
- [ ] `SECRET_KEY` set (generate a strong random key)
- [ ] `DEBUG` set to `True` (dev) or `False` (prod)
- [ ] `ALLOWED_HOSTS` configured
- [ ] `DATABASE_URL` configured (if using PostgreSQL)

### Required for Email Functionality
- [ ] `BREVO_API_KEY` set
- [ ] `BREVO_SENDER_EMAIL` configured
- [ ] `BREVO_SENDER_NAME` set
- [ ] Brevo sender email verified in Brevo dashboard

### Required for Firebase Integration
- [ ] `FIREBASE_TEST_CREDENTIALS_PATH` points to valid JSON file
- [ ] `FIREBASE_PROD_CREDENTIALS_PATH` points to valid JSON file
- [ ] Test service account JSON exists in `firebase-credentials/`
- [ ] Prod service account JSON exists in `firebase-credentials/`
- [ ] Firebase credentials have correct permissions (600)

### Required for Each Product
- [ ] `BETA_HEALTH_APP_TOKEN` set (strong random token)
- [ ] `BETA_HEALTH_TEST_TENANT_ID` configured
- [ ] `BETA_HEALTH_PROD_TENANT_ID` configured
- [ ] `EHR_APP_TOKEN` set (strong random token)
- [ ] `EHR_TEST_TENANT_ID` configured
- [ ] `EHR_PROD_TENANT_ID` configured
- [ ] `EMERGENCY_SERVICE_APP_TOKEN` set (strong random token)
- [ ] `EMERGENCY_SERVICE_TEST_TENANT_ID` configured
- [ ] `EMERGENCY_SERVICE_PROD_TENANT_ID` configured

### Optional but Recommended
- [ ] `SENTRY_DSN` configured for error monitoring
- [ ] `CORS_ALLOWED_ORIGINS` set for your domains
- [ ] `RATE_LIMIT_PER_MINUTE` adjusted if needed
- [ ] `RATE_LIMIT_PER_HOUR` adjusted if needed
- [ ] `LOG_LEVEL` set appropriately

## ✅ Firebase Configuration

- [ ] Firebase project created
- [ ] Multi-tenancy enabled in Firebase
- [ ] Test tenant created and ID noted
- [ ] Production tenant created and ID noted
- [ ] Service account created for test environment
- [ ] Service account created for production environment
- [ ] Service account JSON files downloaded
- [ ] Service account permissions configured
- [ ] Service account JSON files placed in `firebase-credentials/`

## ✅ Brevo Configuration

- [ ] Brevo account created
- [ ] API key generated
- [ ] Sender email added to Brevo
- [ ] Sender email verified
- [ ] API key added to `.env`
- [ ] Test email sent successfully

## ✅ Database Setup

- [ ] Database created (PostgreSQL for production)
- [ ] Database user created with appropriate permissions
- [ ] `DATABASE_URL` configured in `.env`
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Products populated (`python manage.py populate_products`)
- [ ] Superuser created (`python manage.py createsuperuser`)

## ✅ Security Configuration

- [ ] Strong `SECRET_KEY` generated
- [ ] `DEBUG=False` in production
- [ ] HTTPS configured in production
- [ ] SSL certificate installed
- [ ] Firewall rules configured
- [ ] CORS origins properly restricted
- [ ] App tokens are strong and random
- [ ] App tokens not in version control
- [ ] Firebase credentials not in version control
- [ ] `.env` file not in version control

## ✅ Testing

- [ ] Health check endpoint works (`GET /api/health/`)
- [ ] Can authenticate with app token
- [ ] Generic email endpoint works
- [ ] Password reset email works (with Firebase)
- [ ] Forgot password email works (with Firebase)
- [ ] Email verification works (with Firebase)
- [ ] Rate limiting works
- [ ] Error responses are properly formatted
- [ ] Email logs appear in admin panel
- [ ] Django admin accessible

## ✅ Production Deployment (if applicable)

- [ ] Production server provisioned
- [ ] Gunicorn installed and configured
- [ ] Nginx installed and configured
- [ ] Supervisor/systemd service configured
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Database backups configured
- [ ] Log rotation configured
- [ ] Monitoring set up (Sentry, etc.)
- [ ] Health check monitoring configured
- [ ] Firewall rules configured
- [ ] Domain DNS configured

## ✅ Monitoring & Logging

- [ ] Application logs accessible in `logs/django.log`
- [ ] Log rotation configured
- [ ] Sentry error tracking working (if configured)
- [ ] Email delivery monitored in admin panel
- [ ] Performance metrics tracked
- [ ] Uptime monitoring configured

## ✅ Documentation Review

- [ ] README.md reviewed
- [ ] API_DOCUMENTATION.md reviewed
- [ ] DEPLOYMENT.md reviewed (if deploying to production)
- [ ] QUICKSTART.md followed
- [ ] PROJECT_SUMMARY.md reviewed

## ✅ Team Onboarding

- [ ] Development team has access to repository
- [ ] Team members understand authentication flow
- [ ] Team knows how to use admin panel
- [ ] Team knows how to check logs
- [ ] Team knows how to deploy updates
- [ ] Team has access to Brevo dashboard
- [ ] Team has access to Firebase console

## Testing Commands

Use these commands to verify your setup:

```bash
# Activate virtual environment
source venv/bin/activate

# Run system check
python manage.py check

# Test health endpoint
curl http://localhost:8000/api/health/

# Test authenticated endpoint (replace token)
curl -X POST http://localhost:8000/api/email/generic/ \
  -H "Authorization: Bearer YOUR_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "test@example.com",
    "subject": "Test",
    "html_content": "<h1>Test</h1>",
    "environment": "test"
  }'

# Access admin panel
# http://localhost:8000/admin/

# Check logs
tail -f logs/django.log
```

## Common Setup Issues

### Issue: Dependencies won't install
**Check**: Python version is 3.9+
**Fix**: `python3 --version` and upgrade if needed

### Issue: Migrations fail
**Check**: Database connection in `DATABASE_URL`
**Fix**: Test database connection manually

### Issue: "Invalid token" errors
**Check**: Token matches what's in `.env`
**Fix**: Run `python manage.py populate_products` to sync

### Issue: Firebase errors
**Check**: JSON files exist and paths are correct
**Fix**: Verify file paths and permissions

### Issue: Email not sending
**Check**: Brevo API key and sender email verified
**Fix**: Test in Brevo dashboard first

### Issue: Rate limiting not working
**Check**: django-ratelimit installed
**Fix**: `pip install django-ratelimit`

## Environment Variables Generator

Need to generate secure tokens? Use these commands:

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate app tokens
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Next Steps After Setup

1. **Development**
   - Start coding against the API
   - Test all endpoints
   - Review logs regularly

2. **Integration**
   - Update client applications with API endpoints
   - Provide app tokens to each product team
   - Document product-specific configurations

3. **Deployment**
   - Follow DEPLOYMENT.md for production setup
   - Configure monitoring and alerts
   - Set up backup strategy

4. **Maintenance**
   - Monitor email delivery rates
   - Review error logs
   - Update dependencies regularly
   - Rotate tokens periodically

## Support

If you encounter issues not covered in this checklist:
1. Check the logs: `logs/django.log`
2. Review documentation: README.md, API_DOCUMENTATION.md
3. Test individual components (Brevo, Firebase)
4. Check Django system: `python manage.py check`
5. Verify environment variables are loaded correctly

---

**Once all items are checked, your OCM Service Backend is ready to use!** 🎉
