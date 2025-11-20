from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import send_mail
import random
from datetime import timedelta
from Common.models import User, Verification

@api_view(['POST'])
def Register(request):
    try:
        name = request.data.get('us_name')
        email = request.data.get('us_email')
        password = request.data.get('us_password')

        if not name or not email or not password:
            return Response({"error": "Thiếu thông tin bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(us_email=email).exists():
            return Response({"error": "Email đã tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        total_users = User.objects.count()
        new_id = "US" + str(total_users + 1).zfill(3)

        user = User.objects.create(
            us_id=new_id,
            us_name=name,
            us_email=email,
        )
        user.set_password(password)  # hash password

        # Tạo OTP
        otp_code = str(random.randint(100000, 999999))
        start_time = timezone.now()
        end_time = start_time + timedelta(minutes=5)

        Verification.objects.create(
            us=user,
            vc_otp=otp_code,
            vc_start=start_time,
            vc_end=end_time,
            vc_status=False
        )

        # Gửi email (hoặc console backend để test)
        try:
            send_mail(
                subject="Mã OTP xác minh tài khoản",
                message=f"Xin chào {name}, mã OTP của bạn là {otp_code}. Hết hạn sau 5 phút.",
                from_email="hoang7620345@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as mail_error:
            return Response({
                "message": "Đăng ký thành công nhưng gửi OTP thất bại.",
                "error": str(mail_error)
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Đăng ký thành công. Kiểm tra email để xác minh OTP.",
            "user_id": user.us_id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
