from Workspace.models import Task, Subtask
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AddSubtask(APIView):
    def post(self, request, ts_id):
        try:
            data = request.data
            task = Task.objects(ts_id=ts_id).first()

            if not task:
                return Response({"error": "Task không tồn tại"}, status=404)

            new_subtask = Subtask(
                st_id=data.get("st_id"),
                st_title=data.get("st_title"),
                st_subtitle=data.get("st_subtitle"),
                st_note=data.get("st_note", ""),
                st_status=data.get("st_status", False),
                st_start=data.get("st_start"),
                st_end=data.get("st_end")
            )

            task.subtasks.append(new_subtask)
            task.save()

            return Response({"message": "Tạo subtask thành công"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)