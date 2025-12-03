from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import WorkSpace, Member
from datetime import date

class UpdateMemberInWorkspace(APIView):
    def put(self, request, ws_id, us_id):
        try:
            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response({"error": "Workspace không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            member = next((m for m in ws.members if m.us_id == us_id), None)
            if not member:
                return Response({"error": f"Member {us_id} không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            # Cập nhật role hoặc us_img
            role = request.data.get("role")
            us_img = request.data.get("us_img")

            if role:
                member.role = role
            if us_img is not None:
                member.us_img = us_img

            ws.save()
            return Response({"message": f"Member {us_id} cập nhật thành công"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)