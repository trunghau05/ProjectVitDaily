from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from Workspace.models import WorkSpace, Member


class AddMember(APIView):
    def post(self, request):
        try:
            ws_id = request.data.get("ws_id")
            us_id = request.data.get("us_id")
            role = request.data.get("role", "member")

            if not ws_id or not us_id:
                return Response(
                    {"error": "ws_id và us_id là bắt buộc"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response(
                    {"error": "Workspace không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            for m in ws.members:
                if m.us_id == us_id:
                    return Response(
                        {"error": "User đã là thành viên của workspace này"},
                        status=status.HTTP_409_CONFLICT
                    )

            new_member = Member(
                us_id=us_id,
                role=role,
                joined_at=date.today()
            )

            ws.members.append(new_member)
            ws.save()

            return Response({
                "message": "Thêm thành viên thành công!",
                "workspace": {
                    "ws_id": ws.ws_id,
                    "ws_name": ws.ws_name,
                    "ws_label": ws.ws_label,
                    "ws_note": ws.ws_note,
                    "created_at": ws.created_at.isoformat(),
                    "owner_id": ws.owner_id,
                    "members": [
                        {
                            "us_id": m.us_id,
                            "role": m.role,
                            "joined_at": m.joined_at.isoformat()
                        }
                        for m in ws.members
                    ]
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
