from django.urls import path
from .views import get, login, register,otp

urlpatterns = [
    path('user_info/<str:us_id>/', get.get_user_by_id, name='user_info'),
    path('login/', login.Login, name='login'),
    path('register/', register.Register, name='register'),
    path('verify_otp/', otp.VerifyOTP, name='verify_otp'),
    path('email/', get.GetUserByEmail.as_view()),
]