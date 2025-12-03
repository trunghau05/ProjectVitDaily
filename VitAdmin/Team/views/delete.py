from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import Team


class DeleteTeam(APIView):
    def delete(self, request, tm_id):
        try:
            # Lấy team
            team = Team.objects(tm_id=tm_id).first()
            if not team:
                return Response(
                    {"error": f"Team {tm_id} không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Xoá team trong database
            team.delete()

            return Response({
                "message": f"Xoá team {tm_id} thành công!",
                "deleted_team_id": tm_id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
