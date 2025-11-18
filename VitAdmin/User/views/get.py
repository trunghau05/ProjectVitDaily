from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Common.models import User

@api_view(['GET'])
def get_user_by_id(request, us_id):
    try:
        user = User.objects.get(pk=us_id)

        return Response({
            "us_id": user.us_id,
            "us_name": user.us_name,
            "us_email": user.us_email,
            "us_img": user.us_img
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserByEmail(APIView):
    def get(self, request):
        try:
            email = request.query_params.get("us_email")
            if not email:
                return Response({"error": "Missing email"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(us_email=email).values().first()

            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(user, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)