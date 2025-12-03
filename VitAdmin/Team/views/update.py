from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from Workspace.models import *
from Common.models import User


class UpdateTeam(APIView):
    def put(self, request, tm_id):
        try:
            # Lấy team
            team = Team.objects(tm_id=tm_id).first()
            if not team:
                return Response(
                    {"error": f"Team {tm_id} không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Data từ client gửi lên
            tm_name = request.data.get("tm_name")
            tm_desc = request.data.get("tm_desc")
            incoming_members = request.data.get("members", [])

            # Update info team
            if tm_name:
                team.tm_name = tm_name
            if tm_desc is not None:
                team.tm_desc = tm_desc

            # Lấy workspace của team
            workspace = WorkSpace.objects(ws_id=team.ws_id).first()
            if not workspace:
                return Response(
                    {"error": f"Workspace {team.ws_id} không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ================================
            #   STEP 1: XÓA THÀNH VIÊN CŨ
            # ================================
            incoming_ids = {m.get("us_id") for m in incoming_members}

            # Giữ lại thành viên còn tồn tại trong incoming_members
            team.members = [
                member for member in team.members
                if member.us_id in incoming_ids
            ]

            # Build dict sau khi xoá
            current_members_dict = {m.us_id: m for m in team.members}

            skipped_members = []

            # ================================
            #   STEP 2: MERGE & THÊM THÀNH VIÊN MỚI
            # ================================
            for m in incoming_members:
                us_id = m.get("us_id")
                role = m.get("role", "member")

                # Thiếu us_id → bỏ qua
                if not us_id:
                    skipped_members.append({"us_id": None, "reason": "Thiếu us_id"})
                    continue

                # Check User tồn tại
                user = User.objects.filter(us_id=us_id).first()
                if not user:
                    skipped_members.append({"us_id": us_id, "reason": "User không tồn tại"})
                    continue

                # Check xem user có thuộc workspace không
                in_workspace = any(ws_member.us_id == us_id for ws_member in workspace.members)
                if not in_workspace:
                    skipped_members.append({"us_id": us_id, "reason": "Không thuộc workspace"})
                    continue

                # Nếu user đã có trong team -> chỉ update role
                if us_id in current_members_dict:
                    current_members_dict[us_id].role = role
                else:
                    # Thêm mới
                    current_members_dict[us_id] = Member(
                        us_id=user.us_id,
                        us_name=user.us_name,
                        role=role,
                        us_img=user.us_img,
                        joined_at=date.today()
                    )

            # Lưu members mới
            team.members = list(current_members_dict.values())
            team.save()

            # ================================
            #   RESPONSE DỮ LIỆU CHUẨN
            # ================================
            return Response({
                "message": "Cập nhật team thành công!",
                "skipped_members": skipped_members,
                "data": {
                    "tm_id": team.tm_id,
                    "tm_name": team.tm_name,
                    "tm_desc": team.tm_desc,
                    "ws_id": team.ws_id,
                    "created_at": team.created_at.isoformat(),
                    "members": [
                        {
                            "us_id": m.us_id,
                            "us_name": m.us_name,
                            "role": m.role,
                            "us_img": m.us_img,
                            "joined_at": m.joined_at.isoformat() if m.joined_at else None
                        } for m in team.members
                    ]
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
