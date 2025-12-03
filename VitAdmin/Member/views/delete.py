from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import WorkSpace, Member
from datetime import date

class RemoveMemberFromWorkspace(APIView):
    def delete(self, request, ws_id, us_id):
        try:
            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response({"error": "Workspace không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            member_count_before = len(ws.members)
            ws.members = [m for m in ws.members if m.us_id != us_id]

            if len(ws.members) == member_count_before:
                return Response({"error": f"Member {us_id} không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            ws.save()
            return Response({"message": f"Member {us_id} đã được xóa"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
