from Common.models import Task, User, WorkSpace
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def AddTask(request):
    try: 
        total_tasks = Task.objects.count()
        new_id = str(total_tasks + 1).zfill(3)
        
        title = request.data.get('ts_title')
        subtitle = request.data.get('ts_subtitle')
        note = request.data.get('ts_note')
        status_task = request.data.get('ts_status', False)
        start_date = request.data.get('ts_start')
        end_date = request.data.get('ts_end')
        us_id = request.data.get('us_id')
        ws_id = request.data.get('ws_id')

        try:
            user = User.objects.get(pk=us_id)
        except User.DoesNotExist:
            return Response({"error": "User không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            workspace = WorkSpace.objects.get(pk=ws_id)
        except WorkSpace.DoesNotExist:
            return Response({"error": "Workspace không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        
        if not start_date or not end_date:
            return Response({"error": "Ngày bắt đầu và ngày kết thúc là bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)
        if end_date < start_date:
            return Response({"error": "Ngày kết thúc phải sau ngày bắt đầu"}, status=status.HTTP_400_BAD_REQUEST)
        
        task = Task.objects.create(
            ts_id="TS" + new_id,
            ts_title=title,
            ts_subtitle=subtitle,
            ts_note=note,
            ts_status=bool(status_task),
            ts_start=start_date,
            ts_end=end_date,
            us=user,
            ws=workspace
        )

        return Response({
            "message": "Tạo task thành công",
            "task_id": task.ts_id
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)