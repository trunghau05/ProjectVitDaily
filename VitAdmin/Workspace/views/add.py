from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from ..models import WorkSpace, Member


class CreateWorkspace(APIView):
    def post(self, request):
        try:
            ws_name = request.data.get("ws_name")
            ws_label = request.data.get("ws_label")
            ws_note = request.data.get("ws_note", "")
            owner_id = request.data.get("owner_id")

            if not ws_name or not ws_label or not owner_id:
                return Response(
                    {"error": "ws_name, ws_label, owner_id là bắt buộc"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            latest = WorkSpace.objects.order_by("-ws_id").first()
            if latest:
                number = int(latest.ws_id.replace("WS", "")) + 1
            else:
                number = 1

            ws_id = f"WS{number:03d}"

            owner_member = Member(
                role="owner",
                us_id=owner_id,
                joined_at=date.today()
            )
            
            ws = WorkSpace(
                ws_id=ws_id,
                ws_name=ws_name,
                ws_label=ws_label,
                ws_note=ws_note,
                owner_id=owner_id,
                created_at=date.today(),
                members=[owner_member] 
            )
            ws.save()

            return Response({
                "message": "Tạo workspace thành công!",
                "data": {
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
                        } for m in ws.members
                    ]
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
