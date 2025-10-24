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

export interface UpdateAppointmentData {
  appointment_date?: string;
  appointment_time?: string;
  reason?: string;
  status?: 'pending' | 'accepted' | 'rejected' | 'cancelled' | 'completed';
  reschedule_reason?: string;
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

  async updateAppointment(id: number, data: UpdateAppointmentData): Promise<Appointment> {
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

