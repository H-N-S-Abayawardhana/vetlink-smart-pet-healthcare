# VetLink Backend Troubleshooting Guide

## Common Issues and Solutions

### 1. Database Connection Issues

#### Problem: "Database connection failed"
**Symptoms:**
- Error: `asyncpg.exceptions.InvalidCatalogNameError: database "vetlink_db" does not exist`
- Error: `asyncpg.exceptions.ConnectionDoesNotExistError: connection was closed in the middle of operation`

**Solutions:**

1. **Create the database:**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE vetlink_db;
   
   # Create user (optional)
   CREATE USER vetlink_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE vetlink_db TO vetlink_user;
   ```

2. **Update your .env file:**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/vetlink_db
   ```

3. **Install required dependencies:**
   ```bash
   pip install asyncpg psycopg2-binary
   ```

### 2. Email Service Issues

#### Problem: "Email configuration incomplete"
**Symptoms:**
- Warning: "Email configuration incomplete, skipping email notification"
- No emails are being sent

**Solutions:**

1. **Configure SMTP settings in .env:**
   ```env
   # For Gmail
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-app-password
   SMTP_FROM_EMAIL=your-email@gmail.com
   SMTP_SECURE=false
   ```

2. **For Gmail, enable 2-factor authentication and create an App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in SMTP_PASS

3. **For other email providers:**
   ```env
   # Outlook/Hotmail
   SMTP_HOST=smtp-mail.outlook.com
   SMTP_PORT=587
   
   # Yahoo
   SMTP_HOST=smtp.mail.yahoo.com
   SMTP_PORT=587
   ```

### 3. Appointment Creation Issues

#### Problem: "Appointment not being saved to database"
**Symptoms:**
- API returns success but appointment doesn't appear in database
- Error: "Failed to create appointment"

**Solutions:**

1. **Check database permissions:**
   ```sql
   -- Grant necessary permissions
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;
   ```

2. **Run database migrations:**
   ```bash
   cd backend
   alembic upgrade head
   ```

3. **Check for validation errors:**
   - Ensure appointment_date is in YYYY-MM-DD format
   - Ensure appointment_time is in HH:MM:SS format
   - Ensure veterinarian_id exists and is active

### 4. Authentication Issues

#### Problem: "Could not validate credentials"
**Symptoms:**
- 401 Unauthorized errors
- JWT token validation failures

**Solutions:**

1. **Set a strong SECRET_KEY in .env:**
   ```env
   SECRET_KEY=your-very-secure-secret-key-here-make-it-long-and-random
   ```

2. **Check token expiration:**
   ```env
   ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
   ```

### 5. CORS Issues

#### Problem: "CORS policy" errors in browser
**Symptoms:**
- Browser blocks requests from frontend
- Error: "Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy"

**Solutions:**

1. **Update CORS settings in main.py:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",
           "https://yourdomain.com",  # Add your production domain
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

## Testing Your Setup

### 1. Run the Test Script
```bash
cd backend
python test_appointment.py
```

This will test:
- Database connection
- User creation
- Appointment creation
- Email service

### 2. Manual API Testing

#### Test Authentication:
```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

#### Test Appointment Creation:
```bash
# Create appointment (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "veterinarian_id": 2,
    "appointment_date": "2024-01-15",
    "appointment_time": "10:00:00",
    "reason": "Checkup"
  }'
```

## Environment Setup Checklist

- [ ] PostgreSQL is running
- [ ] Database `vetlink_db` exists
- [ ] User has database permissions
- [ ] `.env` file is configured
- [ ] All Python dependencies are installed
- [ ] Database migrations are run
- [ ] SMTP settings are configured (for emails)
- [ ] CORS is configured for your frontend

## Logs and Debugging

### Enable Debug Logging
Add to your `.env` file:
```env
ENVIRONMENT=development
```

### Check Application Logs
The application logs important events. Look for:
- Database connection messages
- Email sending attempts
- Authentication events
- Error messages

### Database Logs
Check PostgreSQL logs for connection issues:
```bash
# On Ubuntu/Debian
sudo tail -f /var/log/postgresql/postgresql-*.log

# On macOS with Homebrew
tail -f /usr/local/var/log/postgres.log
```

## Getting Help

If you're still having issues:

1. **Check the logs** for specific error messages
2. **Run the test script** to identify which component is failing
3. **Verify your environment** against the checklist above
4. **Test each component individually** (database, email, API)

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `database "vetlink_db" does not exist` | Database not created | Create database in PostgreSQL |
| `Email configuration incomplete` | SMTP not configured | Set up SMTP settings in .env |
| `Could not validate credentials` | JWT issues | Check SECRET_KEY and token |
| `CORS policy` | Frontend blocked | Update CORS settings |
| `connection was closed` | Database connection lost | Check database server and credentials |

