from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Common.models import Note

@api_view(['DELETE'])
def DeleteNote(request, nt_id):
    try:
        note = Note.objects.get(nt_id=nt_id)
        note.delete()
        return Response({'message': 'Ghi chú đã được xóa thành công.'}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({'error': 'Ghi chú không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
