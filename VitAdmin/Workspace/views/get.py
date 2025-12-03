from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import WorkSpace

class GetOwnerWorkSpace(APIView):
    def get(self, request):
        try:
            us_id = request.GET.get("us_id")
            if not us_id:
                return Response({"error": "Thiếu us_id"}, status=status.HTTP_400_BAD_REQUEST)

            workspaces = WorkSpace.objects(owner_id=us_id).order_by('-created_at')

            data = [
                {
                    "ws_id": ws.ws_id,
                    "ws_name": ws.ws_name,
                    "ws_label": ws.ws_label,
                    "ws_note": ws.ws_note,
                    "created_at": ws.created_at.isoformat() if ws.created_at else None,
                    "owner_id": ws.owner_id,
                    "members": [
                        {
                            "us_id": m.us_id,
                            "us_name": m.us_name,
                            "us_img": m.us_img or "",
                            "role": m.role,
                            "joined_at": m.joined_at.isoformat() if m.joined_at else None
                        } for m in ws.members
                    ]
                }
                for ws in workspaces
            ]

            return Response({
                "message": "Danh sách workspace user sở hữu",
                "count": len(data),
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetMemberWorkSpace(APIView):
    def get(self, request):
        try:
            us_id = request.GET.get("us_id")
            if not us_id:
                return Response({"error": "Thiếu us_id"}, status=status.HTTP_400_BAD_REQUEST)

            # Query embedded document members
            workspaces = WorkSpace.objects(members__us_id=us_id).order_by('-created_at')

            data = [
                {
                    "ws_id": ws.ws_id,
                    "ws_name": ws.ws_name,
                    "ws_label": ws.ws_label,
                    "ws_note": ws.ws_note,
                    "created_at": ws.created_at.isoformat() if ws.created_at else None,
                    "owner_id": ws.owner_id,
                    "members": [
                        {
                            "us_id": m.us_id,
                            "us_name": m.us_name,
                            "us_img": m.us_img or "",
                            "role": m.role,
                            "joined_at": m.joined_at.isoformat() if m.joined_at else None
                        } for m in ws.members
                    ]
                }
                for ws in workspaces
            ]

            return Response({
                "message": "Danh sách workspace user tham gia",
                "count": len(data),
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetWorkSpaceDetail(APIView):
    def get(self, request):
        try:
            ws_id = request.GET.get("ws_id")
            if not ws_id:
                return Response({"error": "Thiếu ws_id"}, status=status.HTTP_400_BAD_REQUEST)

            ws = WorkSpace.objects(ws_id=ws_id).first()
            if not ws:
                return Response({"error": f"Workspace {ws_id} không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            data = {
                "ws_id": ws.ws_id,
                "ws_name": ws.ws_name,
                "ws_label": ws.ws_label,
                "ws_note": ws.ws_note,
                "created_at": ws.created_at.isoformat() if ws.created_at else None,
                "owner_id": ws.owner_id,
                "members": [
                    {
                        "us_id": m.us_id,
                        "us_name": m.us_name,
                        "us_img": m.us_img or "",
                        "role": m.role,
                        "joined_at": m.joined_at.isoformat() if m.joined_at else None
                    } for m in ws.members
                ]
            }

            return Response({
                "message": f"Chi tiết workspace {ws_id}",
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)