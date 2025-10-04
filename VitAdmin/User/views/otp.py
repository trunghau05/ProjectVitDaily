from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from Common.models import User, Verification

@api_view(['POST'])
def VerifyOTP(request):
    try:
        email = request.data.get('us_email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Thiếu email hoặc OTP"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(us_email=email)
        except User.DoesNotExist:
            return Response({"error": "Người dùng không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        
        verification = Verification.objects.filter(us=user, vc_otp=otp).order_by('-vc_start').first()
        if not verification:
            return Response({"error": "Mã OTP không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        if now > verification.vc_end:
            return Response({"error": "Mã OTP đã hết hạn"}, status=status.HTTP_400_BAD_REQUEST)


        if verification.vc_status:
            return Response({"message": "OTP này đã được xác minh trước đó"}, status=status.HTTP_200_OK)

        verification.vc_status = True
        verification.save()

        if hasattr(user, 'is_verified'):
            user.is_verified = True
            user.save()

        return Response({"message": "Xác minh OTP thành công"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
