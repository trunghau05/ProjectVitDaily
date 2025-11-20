from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password
from Common.models import User, Verification
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def CheckSession(request):
    user = getattr(request, "user_session", None)
    if not user:
        return Response({"logged_in": False}, status=200)

    return Response({
        "logged_in": True,
        "user": {
            "us_id": user.us_id,
            "us_name": user.us_name,
            "us_email": user.us_email,
            "us_img": user.us_img
        }
    })
