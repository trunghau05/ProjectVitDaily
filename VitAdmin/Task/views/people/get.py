from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Workspace.models import Task


class GetTaskByTeam(APIView):
    def get(self, request, tm_id):
        try:
            # Lấy tất cả task thuộc team
            tasks = Task.objects(tm_id=tm_id)

            if not tasks:
                return Response(
                    {"message": "No tasks found for this team"},
                    status=status.HTTP_404_NOT_FOUND
                )

            data = []

            for t in tasks:
                data.append({
                    "ts_id": t.ts_id,
                    "ts_title": t.ts_title,
                    "ts_subtitle": t.ts_subtitle,
                    "ts_status": t.ts_status,
                    "ts_start": str(t.ts_start),
                    "ts_end": str(t.ts_end),
                    "ts_note": t.ts_note,
                    "owner_id": t.owner_id,
                    "tm_id": t.tm_id,

                    # ===========================
                    #   ASSIGNEES (Member[])
                    # ===========================
                    "assignees": [
                        {
                            "us_id": a.us_id,
                            "us_name": a.us_name,
                            "role": a.role,
                            "us_img": a.us_img,
                            "joined_at": str(a.joined_at)
                        }
                        for a in t.assignees
                    ],

                    # ===========================
                    #   SUBTASKS (Subtask[])
                    # ===========================
                    "subtasks": [
                        {
                            "st_id": s.st_id,
                            "st_title": s.st_title,
                            "st_subtitle": s.st_subtitle,
                            "st_note": s.st_note
                        }
                        for s in t.subtasks
                    ]
                })

            return Response({"tasks": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class GetTaskDetail(APIView):
    def get(self, request, ts_id):
        try:
            # -------------------------------
            #    LẤY 1 TASK THEO ts_id
            # -------------------------------
            try:
                task = Task.objects.get(ts_id=ts_id)
            except Task.DoesNotExist:
                return Response(
                    {"message": "Task not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # -------------------------------
            #    TẠO DATA TRẢ VỀ
            # -------------------------------
            data = {
                "ts_id": task.ts_id,
                "ts_title": task.ts_title,
                "ts_subtitle": task.ts_subtitle,
                "ts_status": task.ts_status,
                "ts_start": str(task.ts_start),
                "ts_end": str(task.ts_end),
                "ts_note": task.ts_note,
                "owner_id": task.owner_id,
                "tm_id": task.tm_id,

                # ===========================
                # ASSIGNEES (Member[])
                # ===========================
                "assignees": [
                    {
                        "us_id": a.us_id,
                        "us_name": a.us_name,
                        "role": a.role,
                        "us_img": a.us_img,
                        "joined_at": str(a.joined_at)
                    }
                    for a in task.assignees
                ],

                # ===========================
                # SUBTASKS (Subtask[]) 
                # Nếu KHÔNG muốn lấy subtask
                # => comment đoạn này
                # ===========================
                "subtasks": [
                    {
                        "st_id": s.st_id,
                        "st_title": s.st_title,
                        "st_subtitle": s.st_subtitle,
                        "st_note": s.st_note
                    }
                    for s in task.subtasks
                ]
            }

            return Response({"task": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )