from Workspace.models import Task, Member, Subtask, Team
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

class UpdateTask(APIView):
    def put(self, request, ts_id):
        try:
            data = request.data

            # Lấy task
            task = Task.objects(ts_id=ts_id).first()
            if not task:
                return Response({"error": "Task không tồn tại"}, status=404)

            # --- Cập nhật team nếu có ---
            if "tm_id" in data:
                team = Team.objects(tm_id=data["tm_id"]).first()
                if not team:
                    return Response({"error": "Team không tồn tại"}, status=400)

                # Kiểm tra assignees có thuộc team không
                team_user_ids = [m.us_id for m in (team.members or [])]
                if "assignees" in data:
                    for a in data["assignees"]:
                        if a.get("us_id") not in team_user_ids:
                            return Response({
                                "error": f"Người dùng {a.get('us_id')} không thuộc team {data['tm_id']}"
                            }, status=400)

                task.tm_id = data["tm_id"]

            # --- Cập nhật các trường cơ bản nếu có gửi lên ---
            primitive_fields = [
                "ts_title", "ts_subtitle", "ts_note",
                "ts_status", "ts_start", "ts_end",
                "owner_id"
            ]
            for field in primitive_fields:
                if field in data and data[field] is not None:
                    # Nếu là ngày tháng, convert sang date object nếu cần
                    if field in ["ts_start", "ts_end"]:
                        if isinstance(data[field], str):
                            task[field] = datetime.strptime(data[field], "%Y-%m-%d").date()
                        else:
                            task[field] = data[field]
                    else:
                        task[field] = data[field]

            # --- Cập nhật assignees nếu gửi ---
            if "assignees" in data:
                task.assignees = [
                    Member(
                        role=a.get("role", ""),
                        us_id=a.get("us_id", ""),
                        us_name=a.get("us_name", ""),
                        us_img=a.get("us_img"),
                        joined_at=datetime.strptime(a.get("joined_at"), "%Y-%m-%d").date()
                        if isinstance(a.get("joined_at"), str) else a.get("joined_at")
                    )
                    for a in data["assignees"]
                ]

            # --- Cập nhật subtasks nếu gửi ---
            if "subtasks" in data:
                task.subtasks = [
                    Subtask(
                        st_id=s.get("st_id", ""),
                        st_title=s.get("st_title", ""),
                        st_subtitle=s.get("st_subtitle"),
                        st_note=s.get("st_note")
                    )
                    for s in data["subtasks"]
                ]

            # Lưu task
            task.save()

            return Response({
                "message": "Update task thành công",
                "ts_id": task.ts_id
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
