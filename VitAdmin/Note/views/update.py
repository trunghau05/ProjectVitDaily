from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Common.models import Note, User
from django.utils.dateparse import parse_datetime

@api_view(['PATCH'])
def UpdateNote(request, nt_id):
    try:
        note = Note.objects.get(nt_id=nt_id)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    title = request.data.get('nt_title', note.nt_title)
    subtitle = request.data.get('nt_subtitle', note.nt_subtitle)
    content = request.data.get('nt_content', note.nt_content)
    img = request.data.get('nt_img', note.nt_img)
    pdf = request.data.get('nt_pdf', note.nt_pdf)
    date_str = request.data.get('nt_date')
    us_id = request.data.get('us')

    # Kiểm tra độ dài content nếu có cập nhật
    if 'nt_content' in request.data and len(content.strip()) < 10:
        return Response({'error': 'Nội dung ghi chú phải có ít nhất 10 ký tự.'}, status=status.HTTP_400_BAD_REQUEST)

    # Gán giá trị mới
    note.nt_title = title
    note.nt_subtitle = subtitle
    note.nt_content = content
    note.nt_img = img
    note.nt_pdf = pdf

    # Cập nhật ngày nếu có
    if date_str:
        note.nt_date = parse_datetime(date_str)

    # Cập nhật người dùng nếu có
    if us_id:
        try:
            note.us = User.objects.get(pk=us_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    note.save()
    return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)
