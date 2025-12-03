from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from ..models import WorkSpace, Member

class UpdateWorkSpace(APIView):
    def put(self, request):
        try:
            ws_id = request.data.get("ws_id")
            if not ws_id:
                return Response({"error": "Thiếu ws_id"}, status=status.HTTP_400_BAD_REQUEST)

            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response({"error": f"Workspace {ws_id} không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            # Cập nhật các trường cơ bản nếu có trong request
            ws_name = request.data.get("ws_name")
            ws_label = request.data.get("ws_label")
            ws_note = request.data.get("ws_note")

            if ws_name:
                ws.ws_name = ws_name
            if ws_label:
                ws.ws_label = ws_label
            if ws_note is not None:  # cho phép xóa note
                ws.ws_note = ws_note

            # Optionally: cập nhật members
            members_data = request.data.get("members")  # array of member dict
            if members_data and isinstance(members_data, list):
                updated_members = []
                for item in members_data:
                    us_id = item.get("us_id")
                    us_name = item.get("us_name")
                    us_img = item.get("us_img", "")
                    role = item.get("role", "member")
                    joined_at = item.get("joined_at")

                    if not us_id or not us_name:
                        continue  # skip invalid member

                    # Nếu joined_at không có, mặc định hôm nay
                    joined_at_date = date.fromisoformat(joined_at) if joined_at else date.today()

                    updated_members.append(
                        Member(
                            us_id=us_id,
                            us_name=us_name,
                            us_img=us_img,
                            role=role,
                            joined_at=joined_at_date
                        )
                    )
                ws.members = updated_members

            # Lưu workspace
            ws.save()

            return Response({
                "message": f"Workspace {ws_id} cập nhật thành công",
                "workspace": {
                    "ws_id": ws.ws_id,
                    "ws_name": ws.ws_name,
                    "ws_label": ws.ws_label,
                    "ws_note": ws.ws_note,
                    "created_at": ws.created_at.isoformat() if ws.created_at else None,
                    "owner_id": ws.owner_id,
                    "members": [
                        {
                            "us_id": m.us_id,
                            "us_name": m.us_name,
                            "us_img": m.us_img or "",
                            "role": m.role,
                            "joined_at": m.joined_at.isoformat() if m.joined_at else None
                        } for m in ws.members
                    ]
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
