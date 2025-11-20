from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password
from Common.models import User, Verification
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def Login(request):
    try:
        email = request.data.get('us_email')
        password = request.data.get('us_password')

        if not email or not password:
            return Response({"error": "Thiếu email hoặc mật khẩu"}, status=400)

        try:
            user = User.objects.get(us_email=email)
        except User.DoesNotExist:
            return Response({"error": "Email không tồn tại"}, status=404)

        # OTP chưa xác minh
        if not Verification.objects.filter(us=user, vc_status=True).exists():
            return Response({"error": "Tài khoản chưa xác minh OTP"}, status=403)

        if user.is_locked():
            remaining = int((user.lock_until - timezone.now()).total_seconds() // 60)
            return Response({"error": f"Tài khoản tạm khóa {remaining} phút"}, status=403)

        if not user.check_password(password):
            user.register_failed_attempt()
            if user.is_locked():
                lock_minutes = int((user.lock_until - timezone.now()).total_seconds() // 60)
                return Response({"error": f"Sai mật khẩu nhiều lần. Khóa {lock_minutes} phút"}, status=403)
            else:
                return Response({"error": f"Sai mật khẩu. Còn {3 - user.failed_attempts} lần thử"}, status=400)

        # Reset lock
        user.reset_lock()

        # =========================
        # 1️⃣ LƯU USER VÀO SESSION
        # =========================
        request.session['user_id'] = user.us_id
        request.session.set_expiry(24 * 60 * 60)  # 24h

        # =========================
        # 2️⃣ TẠO JWT TOKEN CUSTOM
        # =========================
        refresh = RefreshToken()
        refresh['user_id'] = user.us_id  # dùng us_id thay vì id
        access = refresh.access_token

        # =========================
        # 3️⃣ TRẢ KẾT QUẢ
        # =========================
        return Response({
            "message": "Đăng nhập thành công",
            "user": {
                "us_id": user.us_id,
                "us_name": user.us_name,
                "us_email": user.us_email,
                "us_img": user.us_img
            },
            "token": {
                "refresh": str(refresh),
                "access": str(access)
            }
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
