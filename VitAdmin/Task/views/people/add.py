from Workspace.models import Subtask, Task, Member, Team
from rest_framework.views import APIView
from rest_framework.response import Response
import re

class AddTaskPeople(APIView):
    def generate_ts_id(self):
        last_task = Task.objects.order_by("-ts_id").first()
        if not last_task:
            return "TS001"
        match = re.search(r"TS(\d+)", last_task.ts_id)
        if match:
            number = int(match.group(1)) + 1
            return f"TS{number:03d}"
        return "TS001"

    def post(self, request):
        try:
            data = request.data

            # Nếu data là list → nhiều task
            if isinstance(data, list):
                created_tasks = []
                for item in data:
                    task = self._create_task(item)
                    created_tasks.append(task.ts_id)
                return Response({
                    "message": f"Tạo thành công {len(created_tasks)} task!",
                    "tasks": created_tasks
                }, status=201)

            # Nếu data là dict → 1 task
            elif isinstance(data, dict):
                task = self._create_task(data)
                return Response({
                    "message": "Tạo task thành công!",
                    "task": task.ts_id
                }, status=201)

            else:
                return Response({"error": "Dữ liệu không hợp lệ"}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def _create_task(self, data):
        tm_id = data.get("tm_id")

        # --- CHECK THUỘC TEAM ---
        if tm_id:
            team = Team.objects(tm_id=tm_id).first()
            if not team:
                raise Exception(f"Team {tm_id} không tồn tại")
            team_user_ids = [m.us_id for m in team.members]
            for ass in data.get("assignees", []):
                if ass["us_id"] not in team_user_ids:
                    raise Exception(f"Người dùng {ass['us_id']} không thuộc team {tm_id}")

        # --- CREATE ASSIGNEES ---
        assignees = [
            Member(
                role=a.get("role"),
                us_id=a.get("us_id"),
                joined_at=a.get("joined_at")
            )
            for a in data.get("assignees", [])
        ]

        # --- CREATE SUBTASKS ---
        subtasks = [
            Subtask(
                st_id=s.get("st_id"),
                st_title=s.get("st_title"),
                st_subtitle=s.get("st_subtitle"),
                st_note=s.get("st_note", "")
            )
            for s in data.get("subtasks", [])
        ]

        # 🔥 TỰ ĐỘNG TẠO TS_ID
        ts_id = self.generate_ts_id()

        # --- SAVE TASK ---
        task = Task(
            ts_id=ts_id,
            ts_title=data["ts_title"],
            ts_subtitle=data.get("ts_subtitle", ""),
            ts_status=data.get("ts_status", 0),
            ts_start=data["ts_start"],
            ts_end=data["ts_end"],
            ts_note=data.get("ts_note", ""),
            owner_id=data["owner_id"],
            tm_id=tm_id,
            assignees=assignees,
            subtasks=subtasks
        )
        task.save()
        return task
