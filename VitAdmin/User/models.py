from django.db import models

class User(models.Model):
    us_id = models.CharField(primary_key=True, max_length=20)
    us_name = models.CharField(max_length=100)
    us_email = models.CharField(max_length=100)
    us_password = models.CharField(max_length=100)
    us_img = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.us_name
    
class Verification(models.Model):
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    vc_otp = models.CharField(max_length=20)
    vc_start = models.DateField()
    vc_end = models.DateField()
    vc_status = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP {self.vc_otp} - {self.us.us_name}"
