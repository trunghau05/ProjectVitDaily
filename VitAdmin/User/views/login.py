from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Common.models import User, Verification

@api_view(['POST'])
def Login(request):
    try:
        email = request.data.get('us_email')
        password = request.data.get('us_password')

        # Kiểm tra dữ liệu bắt buộc
        if not email or not password:
            return Response({"error": "Thiếu email hoặc mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra user tồn tại
        try:
            user = User.objects.get(us_email=email)
        except User.DoesNotExist:
            return Response({"error": "Email không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra đã xác minh OTP hay chưa
        verification_exists = Verification.objects.filter(us=user, vc_status=True).exists()
        if not verification_exists:
            return Response({"error": "Tài khoản chưa được xác minh OTP"}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra tài khoản đang bị khóa
        if user.is_locked():
            remaining_minutes = int((user.lock_until - timezone.now()).total_seconds() // 60)
            return Response({
                "error": f"Tài khoản tạm khóa. Vui lòng thử lại sau {remaining_minutes} phút."
            }, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra mật khẩu
        if not check_password(password, user.us_password):
            user.register_failed_attempt()

            # Nếu sau khi sai mà bị khóa luôn
            if user.is_locked():
                lock_minutes = int((user.lock_until - timezone.now()).total_seconds() // 60)
                return Response({
                    "error": f"Sai mật khẩu nhiều lần. Tài khoản tạm khóa trong {lock_minutes} phút."
                }, status=status.HTTP_403_FORBIDDEN)

            # Nếu chỉ sai bình thường
            return Response({
                "error": f"Sai mật khẩu. Còn {3 - user.failed_attempts} lần thử trước khi bị khóa."
            }, status=status.HTTP_400_BAD_REQUEST)

        # → Đăng nhập thành công → reset lại failed_attempts
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
