# Frontend API Configuration Guide

This guide explains how to update your React frontend to work with the new Python FastAPI backend.

## API Base URL

Update your API base URL from:
```javascript
// Old Next.js API routes
const API_BASE = '/api'
```

To:
```javascript
// New Python FastAPI backend
const API_BASE = 'http://localhost:8000/api/v1'
```

## Authentication Changes

### 1. Remove NextAuth.js Dependencies

Remove these from your `package.json`:
```json
{
  "next-auth": "^4.24.11"
}
```

### 2. Update Authentication Service

Create a new authentication service (`src/lib/auth-service.ts`):

```typescript
const API_BASE = 'http://localhost:8000/api/v1';

export interface User {
  id: number;
  username: string;
  email: string;
  contact_number?: string;
  user_role: 'USER' | 'VETERINARIAN' | 'SUPER_ADMIN';
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterData {
  username: string;
  email: string;
  contact_number?: string;
  password: string;
}

class AuthService {
  private token: string | null = null;

  constructor() {
    this.token = localStorage.getItem('access_token');
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('access_token', data.access_token);
    return data;
  }

  async register(userData: RegisterData): Promise<User> {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    return response.json();
  }

  async getCurrentUser(): Promise<User> {
    if (!this.token) {
      throw new Error('No token available');
    }

    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to get user info');
    }

    return response.json();
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('access_token');
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }
}

export const authService = new AuthService();
```

### 3. Update Sign-in Form

Update your sign-in form (`src/components/signin/SigninForm.tsx`):

```typescript
import { useState } from 'react';
import { authService } from '@/lib/auth-service';
import { useRouter } from 'next/navigation';

export default function SigninForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authService.login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Your form fields */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {loading ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  );
}
```

## API Service Updates

### 1. Create API Service

Create a new API service (`src/lib/api-service.ts`):

```typescript
const API_BASE = 'http://localhost:8000/api/v1';

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
  }

  async delete<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
  }
}

export const apiService = new ApiService();
```

### 2. Update Appointment Service

Update your appointment service to use the new API:

```typescript
import { apiService } from './api-service';

export interface Appointment {
  id: number;
  user_id: number;
  veterinarian_id: number;
  appointment_date: string;
  appointment_time: string;
  reason?: string;
  status: 'pending' | 'accepted' | 'rejected' | 'cancelled' | 'completed';
  payment_status: 'unpaid' | 'paid' | 'refunded';
  created_at: string;
  updated_at: string;
  confirmed_at?: string;
  completed_at?: string;
  user_name?: string;
  user_email?: string;
  user_contact?: string;
  veterinarian_name?: string;
  veterinarian_email?: string;
  veterinarian_contact?: string;
}

export interface CreateAppointmentData {
  veterinarian_id: number;
  appointment_date: string;
  appointment_time: string;
  reason?: string;
}

export interface AppointmentListResponse {
  appointments: Appointment[];
  total: number;
}

class AppointmentService {
  async getAppointments(status?: string, veterinarianId?: number): Promise<AppointmentListResponse> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (veterinarianId) params.append('veterinarian_id', veterinarianId.toString());
    
    const queryString = params.toString();
    const endpoint = `/appointments${queryString ? `?${queryString}` : ''}`;
    
    return apiService.get<AppointmentListResponse>(endpoint);
  }

  async createAppointment(data: CreateAppointmentData): Promise<Appointment> {
    return apiService.post<Appointment>('/appointments', data);
  }

  async getAppointment(id: number): Promise<Appointment> {
    return apiService.get<Appointment>(`/appointments/${id}`);
  }

  async updateAppointment(id: number, data: Partial<CreateAppointmentData> & { status?: string }): Promise<Appointment> {
    return apiService.put<Appointment>(`/appointments/${id}`, data);
  }

  async cancelAppointment(id: number): Promise<void> {
    return apiService.delete<void>(`/appointments/${id}`);
  }

  async processPayment(id: number, paymentData: { payment_method: string; amount: number; payment_details?: any }): Promise<any> {
    return apiService.post(`/appointments/${id}/payment`, paymentData);
  }
}

export const appointmentService = new AppointmentService();
```

### 3. Update Veterinarian Service

```typescript
import { apiService } from './api-service';

export interface Veterinarian {
  id: number;
  username: string;
  email: string;
  contact_number?: string;
  created_at: string;
  total_appointments: number;
  pending_appointments: number;
  accepted_appointments: number;
}

export interface VeterinarianListResponse {
  success: boolean;
  veterinarians: Veterinarian[];
}

export interface AvailabilitySlot {
  time: string;
  display_time: string;
  available: boolean;
}

export interface VeterinarianAvailabilityResponse {
  success: boolean;
  veterinarian: { id: number; username: string };
  date: string;
  available_slots: AvailabilitySlot[];
  booked_appointments: Array<{ appointment_time: string; status: string }>;
}

class VeterinarianService {
  async getVeterinarians(date?: string): Promise<VeterinarianListResponse> {
    const params = new URLSearchParams();
    if (date) params.append('date', date);
    
    const queryString = params.toString();
    const endpoint = `/veterinarians${queryString ? `?${queryString}` : ''}`;
    
    return apiService.get<VeterinarianListResponse>(endpoint);
  }

  async getVeterinarianAvailability(veterinarianId: number, date: string): Promise<VeterinarianAvailabilityResponse> {
    return apiService.get<VeterinarianAvailabilityResponse>(`/veterinarians/${veterinarianId}/availability?date=${date}`);
  }
}

export const veterinarianService = new VeterinarianService();
```

## Environment Configuration

Create a `.env.local` file in your frontend root:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

Then update your API service to use this:

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';
```

## CORS Configuration

Make sure your Python backend allows requests from your frontend by updating the CORS settings in `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Your Next.js dev server
        "https://yourdomain.com",  # Your production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Migration Checklist

- [ ] Remove NextAuth.js dependencies
- [ ] Create new authentication service
- [ ] Update sign-in and sign-up forms
- [ ] Create API service wrapper
- [ ] Update all API calls to use new endpoints
- [ ] Update environment variables
- [ ] Test all functionality
- [ ] Update error handling
- [ ] Update loading states

## Testing the Integration

1. Start your Python backend: `cd backend && python run.py`
2. Start your React frontend: `npm run dev`
3. Test authentication flow
4. Test appointment scheduling
5. Test all CRUD operations

The new Python backend provides the same functionality as your Next.js API routes but with better performance, type safety, and maintainability.

