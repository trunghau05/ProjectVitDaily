from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    us_id = models.CharField(primary_key=True, max_length=20)
    us_name = models.CharField(max_length=100)
    us_email = models.CharField(max_length=100)
    us_password = models.CharField(max_length=100)
    us_img = models.CharField(max_length=255, blank=True, null=True)

    failed_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(blank=True, null=True)

    def is_locked(self):
        """Kiểm tra tài khoản có bị khóa tạm thời không"""
        if self.lock_until and timezone.now() < self.lock_until:
            return True
        return False

    def reset_lock(self):
        """Reset sau khi đăng nhập thành công"""
        self.failed_attempts = 0
        self.lock_until = None
        self.save()

    def register_failed_attempt(self):
        """Xử lý khi đăng nhập sai"""
        self.failed_attempts += 1
        if self.failed_attempts >= 3:  # Sau 3 lần sai thì khóa 5 phút
            lock_minutes = min(5 * self.failed_attempts, 60)  # Tăng dần tối đa 1 giờ
            self.lock_until = timezone.now() + timedelta(minutes=lock_minutes)
        self.save()

    def __str__(self):
        return self.us_name
    
class Verification(models.Model):
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    vc_otp = models.CharField(max_length=20)
    vc_start = models.DateTimeField()
    vc_end = models.DateTimeField()
    vc_status = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP {self.vc_otp} - {self.us.us_name}"
