# Frontend Migration Guide - Next.js to Python Backend

## ✅ What's Been Done

### 1. **Removed Next.js Backend**
- ❌ Deleted all API routes (`src/app/api/`)
- ❌ Removed NextAuth.js configuration
- ❌ Removed backend dependencies from `package.json`
- ❌ Deleted database connection files
- ❌ Removed email service files
- ❌ Cleaned up authentication guards and utilities

### 2. **Created New Frontend Services**
- ✅ `src/lib/auth-service.ts` - JWT authentication service
- ✅ `src/lib/api-service.ts` - Generic API service wrapper
- ✅ `src/lib/appointment-service.ts` - Appointment management
- ✅ `src/lib/veterinarian-service.ts` - Veterinarian services
- ✅ `src/lib/profile-service.ts` - Profile management
- ✅ `src/components/providers/AuthProvider.tsx` - React context for auth

### 3. **Updated Configuration**
- ✅ Updated `package.json` to remove backend dependencies
- ✅ Created `.env.local` for frontend environment variables
- ✅ Updated `src/app/layout.tsx` to use new AuthProvider

## 🚀 Next Steps

### 1. **Install Dependencies**
```bash
npm install
# or
yarn install
```

### 2. **Update Your Components**

#### Replace NextAuth Usage
**Before (NextAuth):**
```typescript
import { useSession } from 'next-auth/react';

function MyComponent() {
  const { data: session } = useSession();
  // ...
}
```

**After (New Auth Service):**
```typescript
import { useAuth } from '@/components/providers/AuthProvider';

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();
  // ...
}
```

#### Update API Calls
**Before (Next.js API routes):**
```typescript
const response = await fetch('/api/appointments');
```

**After (Python backend):**
```typescript
import { appointmentService } from '@/lib/appointment-service';

const appointments = await appointmentService.getAppointments();
```

### 3. **Update Sign-in/Sign-up Forms**

#### Sign-in Form Example:
```typescript
import { useAuth } from '@/components/providers/AuthProvider';
import { useState } from 'react';

export default function SigninForm() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(email, password);
      // Redirect will be handled by AuthProvider
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Your form fields */}
    </form>
  );
}
```

### 4. **Update Dashboard Components**

#### Appointment List Example:
```typescript
import { useEffect, useState } from 'react';
import { appointmentService, Appointment } from '@/lib/appointment-service';

export default function AppointmentList() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await appointmentService.getAppointments();
        setAppointments(response.appointments);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAppointments();
  }, []);

  // Render appointments...
}
```

## 🔧 Environment Setup

### 1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database and email settings
python run.py
```

### 2. **Frontend Setup**
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. **Environment Variables**
Make sure your `.env.local` file has:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## 📋 Migration Checklist

### Components to Update:
- [ ] `src/components/signin/SigninForm.tsx`
- [ ] `src/components/signup/SignupForm.tsx`
- [ ] `src/components/dashboard/appointment-schedule/AppointmentScheduler.tsx`
- [ ] `src/components/dashboard/appointment-schedule/AppointmentList.tsx`
- [ ] `src/components/dashboard/veterinarian-appointments/VeterinarianAppointmentList.tsx`
- [ ] `src/components/dashboard/profile/page.tsx`
- [ ] Any other components using NextAuth or API routes

### Key Changes:
- [ ] Replace `useSession` with `useAuth`
- [ ] Replace API route calls with service methods
- [ ] Update error handling for new API responses
- [ ] Test authentication flow
- [ ] Test appointment scheduling
- [ ] Test profile updates

## 🐛 Common Issues & Solutions

### 1. **CORS Errors**
Make sure your Python backend allows your frontend origin:
```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. **Authentication Issues**
- Check that the backend is running on port 8000
- Verify JWT token is being stored in localStorage
- Check browser network tab for API call errors

### 3. **API Connection Issues**
- Ensure backend is running: `cd backend && python run.py`
- Check API base URL in `.env.local`
- Verify database connection in backend

## 🎯 Testing

### 1. **Test Authentication**
- Register a new user
- Sign in with existing user
- Check that user data is available in components

### 2. **Test Appointments**
- Create a new appointment
- View appointment list
- Update appointment status (if veterinarian)

### 3. **Test Profile**
- Update user profile information
- Verify changes are saved

## 📚 API Reference

### Authentication Endpoints:
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Appointment Endpoints:
- `GET /api/v1/appointments/` - Get appointments
- `POST /api/v1/appointments/` - Create appointment
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

### Veterinarian Endpoints:
- `GET /api/v1/veterinarians/` - Get veterinarians
- `GET /api/v1/veterinarians/{id}/availability` - Get availability

### Profile Endpoints:
- `PUT /api/v1/profile/update` - Update profile

Your frontend is now ready to work with the Python backend! 🎉

