from Workspace.models import Subtask, Task, Member, Team
from rest_framework.views import APIView
from rest_framework.response import Response

class AddTaskPeople(APIView):
    def post(self, request):
        try:
            data = request.data

            ts_id = data.get("ts_id")
            tm_id = data.get("tm_id")

            if tm_id:
                team = Team.objects(tm_id=tm_id).first()
                if not team:
                    return Response({"error": "Team not found."}, status=400)
                team_user_ids = [m.us_id for m in team.members]

                for ass in data.get("assignees", []):
                    if ass["us_id"] not in team_user_ids:
                        return Response({
                            "error": f"Người dùng {ass['us_id']} không thuộc team {tm_id}"
                        }, status = 400)
                
            assignees = []
            for a in data.get("assignees", []):
                assignees.append(
                    Member(
                        role = a.get("role"),
                        us_id = a.get("us_id"),
                        joined_at =a.get("joined_at")
                    )
                )

            subtasks = []
            for s in data.get("subtasks", []):
                subtasks.append(
                    Subtask(
                        st_id=s.get("st_id"),
                        st_title=s.get("st_title"),
                        st_subtitle=s.get("st_subtitle"),
                        st_note=s.get("st_note", ""),
                        st_status=s.get("st_status", False),
                        st_start=s.get("st_start"),
                        st_end=s.get("st_end")
                    )
                )

            task = Task(
                ts_id=data["ts_id"],
                ts_title=data["ts_title"],
                ts_subtitle=data["ts_subtitle"],
                ts_status=data["ts_status"],
                ts_start=data["ts_start"],
                ts_end=data["ts_end"],
                ts_note=data["ts_note"],
                owner_id=data["owner_id"],
                tm_id = tm_id,
                assignees=assignees,
                subtasks=subtasks
            )

            task.save()

            return Response({
                "message": "Tạo task thành công!",
                "task": {
                    "ts_id": task.ts_id,
                    "title": task.ts_title,
                    "team": task.tm_id,
                    "assignee_count": len(task.assignees),
                    "subtask_count": len(task.subtasks)
                }
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)