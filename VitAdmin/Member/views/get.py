from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import WorkSpace
from Common.models import User


class GetMembersByWorkspace(APIView):
    def get(self, request, ws_id):
        try:
            ws = WorkSpace.objects(ws_id=ws_id).first()

            if not ws:
                return Response(
                    {"error": "Workspace không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            members = []
            for m in ws.members:
                try:
                    user = User.objects.get(pk=m.us_id)
                    members.append({
                        "us_id": m.us_id,
                        "us_name": user.us_name,
                        "us_email": user.us_email,
                        "us_img": user.us_img,
                        "role": m.role,
                        "joined_at": m.joined_at.isoformat()
                    })
                except User.DoesNotExist:
                    members.append({
                        "us_id": m.us_id,
                        "us_name": "Unknown",
                        "us_email": "",
                        "us_img": None,
                        "role": m.role,
                        "joined_at": m.joined_at.isoformat()
                    })

            return Response({"data": members}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
