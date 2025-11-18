import axios from 'axios';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  apiUrl = 'http://127.0.0.1:8000/user/';

  constructor() { }

  async userInfo(us_id: string | null) {
    try {
      const respone = await axios.get(this.apiUrl + 'user_info/' + us_id);
      return respone.data;
    } catch (error) {
      Response.error;
    }
  }

  async getUserByEmail(us_email: string) {
    try {
      const response = await axios.get(this.apiUrl + 'email/', {
        params: { us_email }
      });
      return response.data;
    } catch (error) {
      console.error("Lỗi khi lấy thông tin người dùng theo email:", error);
      throw error;
    }
  }
}
