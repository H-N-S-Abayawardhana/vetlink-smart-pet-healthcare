# VetLink Backend API

A FastAPI-based backend for the VetLink Smart Pet Health Care Management System.

## Features

- **Authentication**: JWT-based authentication with role-based access control
- **User Management**: User registration, login, and profile management
- **Appointment System**: Schedule, manage, and track veterinary appointments
- **Veterinarian Management**: Veterinarian availability and appointment management
- **Admin Panel**: User role management and system administration
- **Email Notifications**: Automated email notifications for appointments
- **Payment Processing**: Basic payment processing for appointments

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation using Python type annotations
- **Alembic**: Database migration tool
- **aiosmtplib**: Async SMTP client for email notifications

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up the database**
   ```bash
   # Make sure PostgreSQL is running
   # Update DATABASE_URL in .env file
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/vetlink_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_SECURE=false

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout user

### Appointments
- `GET /api/v1/appointments/` - Get appointments (filtered by user role)
- `POST /api/v1/appointments/` - Create new appointment
- `GET /api/v1/appointments/{id}` - Get specific appointment
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment
- `POST /api/v1/appointments/{id}/payment` - Process payment

### Veterinarians
- `GET /api/v1/veterinarians/` - Get list of veterinarians
- `GET /api/v1/veterinarians/{id}/availability` - Get veterinarian availability

### Profile
- `PUT /api/v1/profile/update` - Update user profile

### Admin (Super Admin only)
- `GET /api/v1/admin/users/` - Get all users
- `PUT /api/v1/admin/users/{id}/role` - Update user role
- `PUT /api/v1/admin/users/{id}/status` - Update user status

## User Roles

- **USER**: Can schedule appointments, view their own appointments, make payments
- **VETERINARIAN**: Can view their appointments, accept/reject appointments
- **SUPER_ADMIN**: Full system access, user management, all appointments

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `contact_number`: Phone number
- `password_hash`: Hashed password
- `user_role`: USER, VETERINARIAN, or SUPER_ADMIN
- `is_active`: Account status
- `created_at`, `updated_at`, `last_login`: Timestamps

### Appointments Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `veterinarian_id`: Foreign key to users table
- `appointment_date`: Date in YYYY-MM-DD format
- `appointment_time`: Time in HH:MM:SS format
- `reason`: Appointment reason
- `status`: pending, accepted, rejected, cancelled, completed
- `payment_status`: unpaid, paid, refunded
- `reschedule_reason`: Reason for rescheduling
- `rescheduled_from`: Reference to original appointment
- `created_at`, `updated_at`, `confirmed_at`, `completed_at`: Timestamps

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Formatting
```bash
# Format code
black app/

# Sort imports
isort app/
```

## Deployment

### Using Docker
```bash
# Build image
docker build -t vetlink-backend .

# Run container
docker run -p 8000:8000 --env-file .env vetlink-backend
```

### Using Gunicorn
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

