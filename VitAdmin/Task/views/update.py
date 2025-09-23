from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Common.models import Task, User, WorkSpace
from django.utils.dateparse import parse_datetime

@api_view(['PATCH'])
def UpdateTask(request, ts_id):
    try:
        task = Task.objects.get(ts_id=ts_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    title = request.data.get('ts_title', task.ts_title)
    subtitle = request.data.get('ts_subtitle', task.ts_subtitle)
    note = request.data.get('ts_note', task.ts_note)
    status_task = request.data.get('ts_status', False if 'ts_status' in request.data else task.ts_status)
    start_date = request.data.get('ts_start' , task.ts_start)
    end_date = request.data.get('ts_end' , task.ts_end)
    us_id = request.data.get('us')
    ws_id = request.data.get('ws')
    date_str = request.data.get('ts_date')

    if 'ts_title' in request.data and len(title.strip()) < 3:
        return Response({'error': 'Tiêu đề task phải có ít nhất 3 ký tự.'}, status=status.HTTP_400_BAD_REQUEST)
    
    task.ts_title = title
    task.ts_subtitle = subtitle
    task.ts_status = status_task
    task.ts_note = note

    if start_date:
        task.ts_start = parse_datetime(start_date)
    if end_date:
        task.ts_end = parse_datetime(end_date)

    if date_str:
        task.ts_date = parse_datetime(date_str)

    if us_id:
        try:
            task.us = User.objects.get(pk=us_id)
        except User.DoesNotExist:
            return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_400_BAD_REQUEST)
        
    if ws_id:
        try:
            task.ws = WorkSpace.objects.get(pk=ws_id)
        except WorkSpace.DoesNotExist:
            return Response({'error': 'Không tìm thấy không gian làm việc'}, status=status.HTTP_400_BAD_REQUEST)
        
    task.save()
    return Response({'message': 'Sửa thành công'}, status=status.HTTP_200_OK)