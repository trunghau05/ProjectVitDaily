from Workspace.models import Task;
from rest_framework.views import APIView
from rest_framework.response import Response

class ListSubtasks(APIView):
    def get(self, request, ts_id):
        task = Task.objects(ts_id=ts_id).first()

        if not task:
            return Response({"error": "Task không tồn tại"}, status=404)

        data = [{
            "st_id": s.st_id,
            "st_title": s.st_title,
            "st_subtitle": s.st_subtitle,
            "st_note": s.st_note,
            "st_status": s.st_status,
            "st_start": s.st_start,
            "st_end": s.st_end,
        } for s in task.subtasks]

        return Response({"subtasks": data}, status=200)
