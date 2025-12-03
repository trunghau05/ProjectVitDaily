export interface User {
  us_id: string;
  us_name: string;
  us_email: string;
  us_password?: string;
  us_img?: string | null;

  failed_attempts?: number;
  lock_until?: string | null;
}

export interface RegisterRequest {
  us_name: string;
  us_email: string;
  us_password: string;
}

export interface RegisterResponse {
  message: string;
  user_id: string;
}

export interface VerifyOtpRequest {
  us_email: string;
  otp: string;
}

export interface VerifyOtpResponse {
  message: string;
}

export interface LoginRequest {
  us_email: string;
  us_password: string;
}

export interface LoginResponse {
  message: string;
  user: User;
}
