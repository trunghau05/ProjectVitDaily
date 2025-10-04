from django.urls import path
from .views import get, login, register,otp

urlpatterns = [
    path('get_user_by_id/<str:us_id>/', get.get_user_by_id, name='get_user_by_id'),
    path('login/', login.Login, name='login'),
    path('register/', register.Register, name='register'),
    path('verify_otp/', otp.VerifyOTP, name='verify_otp'),
]