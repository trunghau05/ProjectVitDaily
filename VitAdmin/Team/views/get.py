from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import *


class GetTeamByWorkspace(APIView):
    def get(self, request):
        try:
            ws_id = request.GET.get("ws_id")
            if not ws_id:
                return Response(
                    {"error": "Thiếu ws_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            teams = Team.objects(ws_id=ws_id).order_by('-created_at')

            data = []
            for t in teams:
                data.append({
                    "tm_id": t.tm_id,
                    "tm_name": t.tm_name,
                    "tm_desc": t.tm_desc,
                    "ws_id": t.ws_id,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                })

            return Response({
                "message": f"Danh sách team trong workspace {ws_id}",
                "count": len(data),
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetTeamDetail(APIView):
    def get(self, request):
        try:
            tm_id = request.GET.get("tm_id")
            if not tm_id:
                return Response(
                    {"error": "Thiếu tm_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            team = Team.objects(tm_id=tm_id).first()
            if not team:
                return Response(
                    {"error": f"Team {tm_id} không tồn tại"},
                    status=status.HTTP_404_NOT_FOUND
                )

            tasks = Task.objects(tm_id=tm_id).order_by('-ts_start')

            task_data = []
            for t in tasks:
                task_data.append({
                    "ts_id": t.ts_id,
                    "ts_title": t.ts_title,
                    "ts_subtitle": t.ts_subtitle,
                    "ts_status": t.ts_status,
                    "ts_start": t.ts_start.isoformat() if t.ts_start else None,
                    "ts_end": t.ts_end.isoformat() if t.ts_end else None,
                    "ts_note": t.ts_note,
                    "owner_id": t.owner_id,
                    "assignees": [
                        {
                            "us_id": a.us_id,
                            "us_name": a.us_name,
                            "us_img": a.us_img or "",
                            "role": a.role,
                            "joined_at": a.joined_at.isoformat() if a.joined_at else None
                        }
                        for a in t.assignees
                    ],
                    "subtasks": [
                        {
                            "st_id": st.st_id,
                            "st_title": st.st_title,
                            "st_subtitle": st.st_subtitle,
                            "st_note": st.st_note,
                        }
                        for st in t.subtasks
                    ],
                })

            # --- Serialize members của team ---
            members_data = [
                {
                    "us_id": m.us_id,
                    "us_name": m.us_name,
                    "us_img": m.us_img or "",
                    "role": m.role,
                    "joined_at": m.joined_at.isoformat() if m.joined_at else None
                }
                for m in team.members
            ]

            data = {
                "tm_id": team.tm_id,
                "tm_name": team.tm_name,
                "tm_desc": team.tm_desc,
                "ws_id": team.ws_id,
                "created_at": team.created_at.isoformat() if team.created_at else None,
                "members": members_data,  # <<< Thêm phần này
                "tasks": task_data
            }

            return Response({
                "message": f"Chi tiết team {tm_id}",
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
