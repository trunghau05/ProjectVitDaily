from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password
from Common.models import User, Verification
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def Login(request):
    try:
        email = request.data.get('us_email')
        password = request.data.get('us_password')

        if not email or not password:
            return Response({"error": "Thiếu email hoặc mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(us_email=email)
        except User.DoesNotExist:
            return Response({"error": "Email không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        #Kiểm tra đã xác minh OTP chưa
        verification = Verification.objects.filter(us=user, vc_status=True).exists()
        if not verification:
            return Response({"error": "Tài khoản chưa được xác minh OTP"}, status=status.HTTP_403_FORBIDDEN)

        #Kiểm tra tài khoản đang bị khóa tạm thời
        if user.is_locked():
            remaining = int((user.lock_until - timezone.now()).total_seconds() // 60)
            return Response({
                "error": f"Tài khoản tạm khóa. Vui lòng thử lại sau {remaining} phút."
            }, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra mật khẩu
        if not check_password(password, user.us_password):
            user.register_failed_attempt()
            if user.is_locked():
                lock_minutes = int((user.lock_until - timezone.now()).total_seconds() // 60)
                return Response({
                    "error": f"Sai mật khẩu nhiều lần. Tài khoản tạm khóa trong {lock_minutes} phút."
                }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "error": f"Sai mật khẩu. Còn {3 - user.failed_attempts} lần thử trước khi bị khóa."
                }, status=status.HTTP_400_BAD_REQUEST)

        #Đăng nhập thành công → reset lại bộ đếm
        user.reset_lock()

        return Response({
            "message": "Đăng nhập thành công",
            "user": {
                "us_id": user.us_id,
                "us_name": user.us_name,
                "us_email": user.us_email,
                "us_img": user.us_img
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
