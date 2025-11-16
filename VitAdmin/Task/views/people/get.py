from Workspace.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response

class GetTask(APIView):
    def get(self, request, tm_id):
        tasks = Task.objects(tm_id=tm_id)

        result = []
        for t in tasks:
            result.append({
                "ts_id": t.ts_id,
                "ts_title": t.ts_title,
                "ts_status": t.ts_status,
                "ts_start": t.ts_start,
                "ts_end": t.ts_end,
                "assignee_count": len(t.assignees),
                "subtask_count": len(t.subtasks)
            })

        return Response({
            "team_id": tm_id,
            "total": len(result),
            "tasks": result
        })
