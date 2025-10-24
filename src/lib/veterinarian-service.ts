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

