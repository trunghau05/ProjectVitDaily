from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import WorkSpace

class DeleteWorkSpace(APIView):
    def delete(self, request, ws_id):
        try:
            # Lấy workspace theo ws_id
            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response({"error": f"Workspace {ws_id} không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            # Lấy current_user_id từ query param, header hoặc session
            current_user_id = request.GET.get("current_user_id")
            if not current_user_id:
                return Response({"error": "Thiếu current_user_id"}, status=status.HTTP_400_BAD_REQUEST)

            # Chỉ owner mới được xóa workspace
            if ws.owner_id != current_user_id:
                return Response({"error": "Chỉ owner mới có quyền xóa workspace"}, status=status.HTTP_403_FORBIDDEN)

            # Xóa workspace
            ws.delete()
            return Response({"message": f"Workspace {ws_id} đã được xóa thành công"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
