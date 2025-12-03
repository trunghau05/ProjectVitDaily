from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from Workspace.models import *
import json


class AddMembers(APIView):
    def post(self, request):
        try:
            ws_id = request.data.get("ws_id")
            members_data = request.data.get("members", [])

            if not ws_id:
                return Response({"error": "ws_id là bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(members_data, list) or len(members_data) == 0:
                return Response({"error": "members phải là một danh sách chứa ít nhất 1 member"}, status=status.HTTP_400_BAD_REQUEST)

            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response({"error": "Workspace không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            added_members = []
            skipped_members = []

            for item in members_data:
                us_id = item.get("us_id")
                us_name = item.get("us_name")
                us_img = item.get("us_img", "")
                role = item.get("role", "member")

                # Check thiếu dữ liệu
                if not us_id or not us_name:
                    skipped_members.append({
                        "data": item,
                        "reason": "Thiếu us_id hoặc us_name"
                    })
                    continue

                # Check đã tồn tại trong workspace?
                if any(m.us_id == us_id for m in ws.members):
                    skipped_members.append({
                        "us_id": us_id,
                        "reason": "Đã là thành viên"
                    })
                    continue

                # Tạo Member
                new_member = Member(
                    us_id=us_id,
                    us_name=us_name,
                    us_img=us_img,
                    role=role,
                    joined_at=date.today()
                )

                ws.members.append(new_member)
                added_members.append(us_id)

            # Lưu workspace
            ws.save()

            # ==========================
            # Response
            # ==========================
            return Response({
                "message": "Thêm nhiều thành viên hoàn tất",
                "added": added_members,
                "skipped": skipped_members,
                "workspace": {
                    "ws_id": ws.ws_id,
                    "ws_name": ws.ws_name,
                    "ws_label": ws.ws_label,
                    "ws_note": ws.ws_note,
                    "owner_id": ws.owner_id,
                    "created_at": ws.created_at.isoformat(),
                    "members": [
                        {
                            "us_id": m.us_id,
                            "us_name": m.us_name,
                            "us_img": m.us_img,
                            "role": m.role,
                            "joined_at": m.joined_at.isoformat()
                        }
                        for m in ws.members
                    ]
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddMemberToTeam(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            tm_id = data.get("tm_id")
            ws_id = data.get("ws_id")
            us_id = data.get("us_id")
            us_name = data.get("us_name")
            role = data.get("role")
            us_img = data.get("us_img", "")

            # Kiểm tra bắt buộc
            if not all([tm_id, ws_id, us_id, us_name, role]):
                return Response(
                    {"error": "Thiếu thông tin bắt buộc"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Lấy team
            team = Team.objects(tm_id=tm_id, ws_id=ws_id).first()
            if not team:
                return Response(
                    {"error": f"Team {tm_id} trong workspace {ws_id} không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Kiểm tra thành viên đã tồn tại chưa
            if any(m.us_id == us_id for m in team.members):
                return Response(
                    {"error": f"Thành viên {us_id} đã có trong team"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Tạo Member mới
            new_member = Member(
                us_id=us_id,
                us_name=us_name,
                role=role,
                us_img=us_img,
                joined_at=date.today()
            )

            # Thêm vào team
            team.members.append(new_member)
            team.save()

            # Trả về team mới
            members_data = [
                {
                    "us_id": m.us_id,
                    "us_name": m.us_name,
                    "role": m.role,
                    "us_img": m.us_img,
                    "joined_at": m.joined_at.isoformat()
                }
                for m in team.members
            ]

            return Response({
                "message": f"Đã thêm thành viên {us_id} vào team {tm_id}",
                "team_id": tm_id,
                "members": members_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)