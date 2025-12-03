from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import random
from datetime import timedelta
from Common.models import User, Verification

@api_view(['POST'])
def Register(request):
    try:
        # Nhận dữ liệu từ client
        name = request.data.get('us_name')
        email = request.data.get('us_email')
        password = request.data.get('us_password')

        # Kiểm tra dữ liệu
        if not all([name, email, password]):
            return Response({"error": "Thiếu thông tin bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra email tồn tại
        if User.objects.filter(us_email=email).exists():
            return Response({"error": "Email đã tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo user_id tự động
        total_users = User.objects.count()
        new_id = "US" + str(total_users + 1).zfill(3)

        # Tạo user mới
        user = User.objects.create(
            us_id=new_id,
            us_name=name,
            us_email=email,
            us_password=make_password(password)
        )

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

        # Gửi email OTP
        try:
            send_mail(
                "Mã OTP xác minh tài khoản",
                f"Xin chào {name},\n\nMã OTP của bạn là: {otp_code}\nCó hiệu lực trong 5 phút.",
                "hoang7620345@gmail.com",
                [email],
                fail_silently=False,
            )
        except Exception as mail_error:
            return Response({
                "message": "Đăng ký thành công nhưng gửi OTP thất bại.",
                "error": str(mail_error)
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Đăng ký thành công. Vui lòng kiểm tra email để xác minh OTP.",
            "user_id": user.us_id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
