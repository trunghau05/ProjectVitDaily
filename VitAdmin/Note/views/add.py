from django.utils import timezone
from Common.models import Note, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def AddNote(request):
    try:
        total_notes = Note.objects.count()
        new_id = str(total_notes + 1).zfill(3) 

        title = request.data.get('nt_title')
        subtitle = request.data.get('nt_subtitle')
        content = request.data.get('nt_content')
        img = request.data.get('nt_img')
        pdf = request.data.get('nt_pdf')
        us_id = request.data.get('us_id')

        try:
            user = User.objects.get(pk=us_id)
        except User.DoesNotExist:
            return Response({"error": "User không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        if content and len(content) < 10:
            return Response({"error": "Nội dung phải có ít nhất 10 ký tự"}, status=status.HTTP_400_BAD_REQUEST)

        note = Note.objects.create(
            nt_id="NT" + new_id,
            nt_title=title,
            nt_subtitle=subtitle,
            nt_content=content,
            nt_img=img,
            nt_pdf=pdf,
            nt_date=timezone.now(),
            us=user
        )

        return Response({
            "message": "Tạo note thành công",
            "note_id": note.nt_id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
