from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from Workspace.models import *
from Common.models import User   # <<< lấy thông tin owner nếu cần

class CreateTeam(APIView):
    def post(self, request):
        try:
            tm_name = request.data.get("tm_name")
            tm_desc = request.data.get("tm_desc", "")
            ws_id = request.data.get("ws_id")
            members = request.data.get("members", [])  # danh sách member gửi lên, optional

            # Validate input
            if not tm_name or not ws_id:
                return Response(
                    {"error": "tm_name và ws_id là bắt buộc"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra workspace tồn tại
            workspace = WorkSpace.objects(ws_id=ws_id).first()
            if not workspace:
                return Response(
                    {"error": f"Workspace {ws_id} không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Tạo tm_id tự động theo thứ tự
            latest = Team.objects.order_by("-tm_id").first()
            number = int(latest.tm_id.replace("TM", "")) + 1 if latest else 1
            tm_id = f"TM{number:03d}"

            # Chuyển members JSON sang EmbeddedDocument Member
            member_objs = []
            for m in members:
                us_id = m.get("us_id")
                role = m.get("role", "member")
                
                # Kiểm tra user có tồn tại trong hệ thống
                user = User.objects.filter(us_id=us_id).first()
                if not user:
                    continue  # bỏ qua nếu không tìm thấy user
                
                # Kiểm tra user có thuộc workspace không
                in_workspace = any(ws_member.us_id == us_id for ws_member in workspace.members)
                if not in_workspace:
                    continue  # bỏ qua nếu user không thuộc workspace

                member_objs.append(
                    Member(
                        us_id=user.us_id,
                        us_name=user.us_name,
                        role=role,
                        us_img=user.us_img,
                        joined_at=date.today()
                    )
                )

            # Tạo team
            team = Team(
                tm_id=tm_id,
                tm_name=tm_name,
                tm_desc=tm_desc,
                ws_id=ws_id,
                created_at=date.today(),
                members=member_objs
            )
            team.save()

            # Response
            return Response({
                "message": "Tạo team thành công!",
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
                            "joined_at": m.joined_at.isoformat()
                        } for m in team.members
                    ]
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
