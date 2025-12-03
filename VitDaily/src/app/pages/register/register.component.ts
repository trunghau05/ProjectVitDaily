import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FlexCenterDirective } from '../../directives/flex-center/flex-center.directive';
import { UserService } from '../../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [CommonModule, FormsModule, FlexCenterDirective],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  name: string = '';
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  otp: string = '';
  loading: boolean = false;
  errorMessage: string = '';
  successMessage: string = '';
  showOtpPopup: boolean = false;

  constructor(private userService: UserService, private router: Router) {}

  async register() {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.name || !this.email || !this.password || !this.confirmPassword) {
      this.errorMessage = 'Vui lòng điền đầy đủ thông tin';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Mật khẩu nhập lại không khớp';
      return;
    }

    this.loading = true;

    try {
      const response = await this.userService.register({
        us_name: this.name,
        us_email: this.email,
        us_password: this.password
      });

      if (response && response.user_id) {
        this.successMessage = response.message || 'Đăng ký thành công';
        this.showOtpPopup = true;
      } else {
        this.errorMessage = response?.error || 'Đăng ký thất bại';
      }
    } catch (error: any) {
      this.errorMessage = error?.response?.data?.error || 'Có lỗi xảy ra';
    } finally {
      this.loading = false;
    }
  }

  async verifyOtp() {
    if (!this.otp) {
      this.errorMessage = 'Vui lòng nhập OTP';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    try {
      const response = await this.userService.verifyOtp({
        us_email: this.email,
        otp: this.otp
      });

      if (response?.message) {
        this.successMessage = response.message;
        this.showOtpPopup = false;

        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1000);
      } else {
        this.errorMessage = response?.error || 'Xác minh OTP thất bại';
      }
    } catch (error: any) {
      this.errorMessage = error?.response?.data?.error || 'Có lỗi xảy ra';
    } finally {
      this.loading = false;
    }
  }
}