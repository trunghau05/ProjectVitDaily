from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Common.models import Task, User, WorkSpace

@api_view(['DELETE'])
def DeleteTask(request, ts_id):
    try:
        task = Task.objects.get(ts_id=ts_id)
        task.delete()
        return Response({'message': 'Task đã được xóa thành công.'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Task không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)