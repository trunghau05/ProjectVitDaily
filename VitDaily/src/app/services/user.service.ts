import axios from 'axios';
import { Injectable } from '@angular/core';
import { User } from '../models/user.interface';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiUrl = 'http://127.0.0.1:8000/user/';

  constructor() {}

  async userInfo(us_id: string | null) {
    if (!us_id) return null;
    try {
      const response = await axios.get(`${this.apiUrl}user_info/${us_id}/`);
      return response.data;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  async getUserByEmail(us_email: string) {
    try {
      const response = await axios.get(`${this.apiUrl}email/`, { params: { us_email } });
      return response.data;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  async register(data: { us_name: string; us_email: string; us_password: string }) {
    try {
      const response = await axios.post(`${this.apiUrl}register/`, data);
      return response.data;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  async verifyOtp(data: { us_email: string; otp: string }) {
    try {
      const response = await axios.post(`${this.apiUrl}verify_otp/`, data);
      return response.data;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  async login(data: { us_email: string; us_password: string }) {
    try {
      const response = await axios.post(`${this.apiUrl}login/`, data);
      return response.data;
    } catch (error) {
      console.error(error);
      return null;
    }
  }
  
}
