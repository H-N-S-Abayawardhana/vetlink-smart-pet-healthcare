import { apiService } from './api-service';
import { User } from './auth-service';

export interface UpdateProfileData {
  username?: string;
  email?: string;
  contact_number?: string;
}

class ProfileService {
  async updateProfile(data: UpdateProfileData): Promise<User> {
    return apiService.put<User>('/profile/update', data);
  }
}

export const profileService = new ProfileService();

