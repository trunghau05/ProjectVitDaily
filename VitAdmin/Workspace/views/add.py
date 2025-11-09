from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from ..models import *


class InsertSampleData(APIView):
    def post(self, request):
        try:
            # -----------------------------
            # 1️⃣ WORKSPACE
            # -----------------------------
            ws = WorkSpace(
                ws_id="WS001",
                ws_name="PonPlan Project Workspace",
                owner_id="admin01"
            )
            ws.save()

            # -----------------------------
            # 2️⃣ TEAMS
            # -----------------------------
            # ---- Frontend Team ----
            fe_members = [
                Member(role="Team Leader", us_id="user001", joined_at=date(2025, 1, 2)),
                Member(role="UI Developer", us_id="user002", joined_at=date(2025, 1, 5)),
                Member(role="UX Designer", us_id="user003", joined_at=date(2025, 1, 8)),
            ]
            fe_team = Team(
                tm_id="T001",
                tm_name="Frontend Team",
                tm_desc="Phát triển giao diện Ionic/Angular",
                members=fe_members,
                created_at=date(2025, 1, 1),
                ws_id=ws.ws_id
            )
            fe_team.save()

            # ---- Backend Team ----
            be_members = [
                Member(role="Team Leader", us_id="user004", joined_at=date(2025, 1, 3)),
                Member(role="API Developer", us_id="user005", joined_at=date(2025, 1, 6)),
                Member(role="Database Engineer", us_id="user006", joined_at=date(2025, 1, 10)),
            ]
            be_team = Team(
                tm_id="T002",
                tm_name="Backend Team",
                tm_desc="Xử lý API Django + MongoDB + Firebase",
                members=be_members,
                created_at=date(2025, 1, 2),
                ws_id=ws.ws_id
            )
            be_team.save()

            # -----------------------------
            # 3️⃣ HÀM HỖ TRỢ: Lấy Member theo us_id
            # -----------------------------
            def get_member_from_team(team_members, us_id):
                for m in team_members:
                    if m.us_id == us_id:
                        return m
                return None  # Nếu không thấy, trả None

            # -----------------------------
            # 4️⃣ TASKS THEO TEAM (role đồng bộ)
            # -----------------------------
            # --- Task 1: Frontend Team ---
            fe_subtasks = [
                Subtask(
                    st_id="ST001",
                    st_title="Thiết kế giao diện Dashboard",
                    st_subtitle="Dùng Figma tạo layout tổng thể",
                    st_note="Tập trung vào UX người dùng gia đình",
                    st_status=True,
                    st_start=date(2025, 1, 3),
                    st_end=date(2025, 1, 6)
                ),
                Subtask(
                    st_id="ST002",
                    st_title="Code giao diện Dashboard",
                    st_subtitle="Angular + Ionic Components",
                    st_note="Áp dụng theme sáng/tối tự động",
                    st_status=False,
                    st_start=date(2025, 1, 7),
                    st_end=date(2025, 1, 15)
                ),
            ]

            fe_task_assignees = [
                get_member_from_team(fe_team.members, "user002"),  # UI Developer
                get_member_from_team(fe_team.members, "user003"),  # UX Designer
            ]

            fe_task = Task(
                ts_id="TS001",
                ts_title="Xây dựng giao diện Dashboard PonPlan",
                ts_subtitle="Giao diện người dùng chính",
                ts_status=False,
                ts_start=date(2025, 1, 3),
                ts_end=date(2025, 1, 20),
                ts_note="Phần quan trọng nhất của sprint đầu tiên",
                owner_id="user001",  # Team Leader
                tm_id=fe_team.tm_id,
                assignees=fe_task_assignees,
                subtasks=fe_subtasks
            )
            fe_task.save()

            # --- Task 2: Backend Team ---
            be_subtasks = [
                Subtask(
                    st_id="ST004",
                    st_title="Thiết kế schema MongoDB",
                    st_subtitle="Model hóa Task, Team, Workspace",
                    st_note="Tối ưu cấu trúc lưu trữ embedded",
                    st_status=True,
                    st_start=date(2025, 1, 4),
                    st_end=date(2025, 1, 6)
                ),
                Subtask(
                    st_id="ST005",
                    st_title="Xây dựng API Task & Team",
                    st_subtitle="Django Rest Framework",
                    st_note="Cần endpoint tạo dữ liệu mẫu",
                    st_status=True,
                    st_start=date(2025, 1, 7),
                    st_end=date(2025, 1, 12)
                ),
            ]

            be_task_assignees = [
                get_member_from_team(be_team.members, "user005"),  # API Developer
                get_member_from_team(be_team.members, "user006"),  # Database Engineer
            ]

            be_task = Task(
                ts_id="TS002",
                ts_title="Xây dựng API và kết nối Firebase",
                ts_subtitle="Phần backend cốt lõi",
                ts_status=False,
                ts_start=date(2025, 1, 4),
                ts_end=date(2025, 1, 20),
                ts_note="Đảm bảo dữ liệu realtime và an toàn",
                owner_id="user004",  # Team Leader
                tm_id=be_team.tm_id,
                assignees=be_task_assignees,
                subtasks=be_subtasks
            )
            be_task.save()

            # --- Task 3: Task cá nhân (không thuộc team) ---
            solo_member = Member(role="Admin", us_id="admin01", joined_at=date(2025, 1, 1))
            solo_task = Task(
                ts_id="TS003",
                ts_title="Viết tài liệu hướng dẫn PonPlan",
                ts_subtitle="Dành cho người dùng mới",
                ts_status=False,
                ts_start=date(2025, 1, 10),
                ts_end=date(2025, 1, 15),
                ts_note="Bao gồm phần cài đặt và cách dùng thẻ chi tiêu",
                owner_id="admin01",
                tm_id=None,
                assignees=[solo_member],
                subtasks=[]
            )
            solo_task.save()

            # -----------------------------
            # ✅ KẾT QUẢ TRẢ VỀ
            # -----------------------------
            return Response({
                "message": "✅ Dữ liệu mẫu (role khớp giữa team & task) đã được tạo!",
                "workspace": ws.ws_name,
                "teams": [fe_team.tm_name, be_team.tm_name],
                "tasks": [fe_task.ts_title, be_task.ts_title, solo_task.ts_title],
                "note": "Các assignee trong Task lấy đúng role từ Team."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
