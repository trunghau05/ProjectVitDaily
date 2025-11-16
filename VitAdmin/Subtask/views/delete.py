from Workspace.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DeleteSubtask(APIView):
    def delete(self, request, ts_id, st_id):
        try:
            task = Task.objects(ts_id=ts_id).first()

            if not task:
                return Response({"error": "Task không tồn tại"}, status=404)

            before = len(task.subtasks)
            task.subtasks = [s for s in task.subtasks if s.st_id != st_id]
            after = len(task.subtasks)

            if before == after:
                return Response({"error": "Subtask không tồn tại"}, status=404)

            task.save()
            return Response({"message": "Xóa subtask thành công"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
