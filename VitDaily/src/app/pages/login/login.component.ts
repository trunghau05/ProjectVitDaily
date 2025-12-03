import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../services/user.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  
  email: string = '';
  password: string = '';
  remember: boolean = false;
  loading: boolean = false;
  errorMessage: string = '';
  successMessage: string = '';

  constructor(private userService: UserService, private router: Router) {}

  async login() {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.email || !this.password) {
      this.errorMessage = 'Vui lòng nhập email và mật khẩu';
      return;
    }

    this.loading = true;

    try {
      const response = await this.userService.login({
        us_email: this.email,
        us_password: this.password
      });

      if (response && response.message) {
        this.successMessage = response.message;
        sessionStorage.setItem('us_id', JSON.stringify(response.us_id));

        setTimeout(() => {
          this.router.navigate(['/dashboard']); 
        }, 500);
      } else if (response && response.error) {
        this.errorMessage = response.error;
      } else {
        this.errorMessage = 'Đăng nhập thất bại';
      }
    } catch (error: any) {
      this.errorMessage = error?.response?.data?.error || 'Có lỗi xảy ra';
    } finally {
      this.loading = false;
    }
  }
}