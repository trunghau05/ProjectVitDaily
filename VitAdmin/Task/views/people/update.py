from Workspace.models import Task, Member, Subtask, Team
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UpdateTaskPeople(APIView):
    def put(self, request, ts_id):
        try:
            data = request.data

            
            task = Task.objects(ts_id=ts_id).first()
            if not task:
                return Response({"error": "Task không tồn tại"}, status=404)
            
            tm_id = data.get("tm_id", task.tm_id)
            if tm_id:
                team = Team.objects(tm_id=tm_id).first()
                if not team:
                    return Response({"error": "Team không tồn tại"}, status=400)

                team_members = team.members or []
                team_user_ids = [m.us_id for m in team_members]

                if "assignees" in data:
                    for a in data["assignees"]:
                        if a["us_id"] not in team_user_ids:
                            return Response({
                                "error": f"Người dùng {a['us_id']} không thuộc team {tm_id}"
                            }, status=400)

                task.tm_id = tm_id

            task.ts_title = data.get("ts_title", task.ts_title)
            task.ts_subtitle = data.get("ts_subtitle", task.ts_subtitle)
            task.ts_note = data.get("ts_note", task.ts_note)
            task.ts_status = data.get("ts_status", task.ts_status)
            task.ts_start = data.get("ts_start", task.ts_start)
            task.ts_end = data.get("ts_end", task.ts_end)
            task.owner_id = data.get("owner_id", task.owner_id)

            if "assignees" in data:
                new_assignees = []
                for a in data["assignees"]:
                    new_assignees.append(
                        Member(
                            role=a.get("role"),
                            us_id=a.get("us_id"),
                            joined_at=a.get("joined_at")
                        )
                    )
                task.assignees = new_assignees

            if "subtasks" in data:
                new_subtasks = []
                for s in data["subtasks"]:
                    new_subtasks.append(
                        Subtask(
                            st_id=s.get("st_id"),
                            st_title=s.get("st_title"),
                            st_subtitle=s.get("st_subtitle"),
                            st_note=s.get("st_note", ""),
                            st_status=s.get("st_status"),
                            st_start=s.get("st_start"),
                            st_end=s.get("st_end")
                        )
                    )
                task.subtasks = new_subtasks

            task.save()

            return Response({
                "message": "Update task thành công",
                "task": {
                    "ts_id": task.ts_id,
                    "title": task.ts_title,
                    "assignees": len(task.assignees),
                    "subtasks": len(task.subtasks),
                    "team": task.tm_id
                }
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
