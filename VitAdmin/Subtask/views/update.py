from Workspace.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class UpdateSubtask(APIView):
    def put(self, request, ts_id, st_id):
        try:
            data = request.data
            task = Task.objects(ts_id=ts_id).first()

            if not task:
                return Response({"error": "Task không tồn tại"}, status=404)

            for s in task.subtasks:
                if s.st_id == st_id:
                    s.st_title = data.get("st_title", s.st_title)
                    s.st_subtitle = data.get("st_subtitle", s.st_subtitle)
                    s.st_note = data.get("st_note", s.st_note)
                    s.st_status = data.get("st_status", s.st_status)
                    s.st_start = data.get("st_start", s.st_start)
                    s.st_end = data.get("st_end", s.st_end)
                    task.save()
                    return Response({"message": "Update subtask thành công"}, status=200)

            return Response({"error": "Subtask không tồn tại"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
