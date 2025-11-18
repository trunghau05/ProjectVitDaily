from Workspace.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DeleteTaskPeople(APIView):
    def delete(self, request, ts_id):
        try:
            task = Task.objects(ts_id = ts_id).first()

            if not task:
                return Response(
                    {"error": f"Task {ts_id} không tồn tại"},
                    status = status.HTTP_404_NOT_FOUND
                )
            task.delete()

            return Response(
                {"erros": f"Xóa task {ts_id} thành công"},
                status = status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)