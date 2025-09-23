from rest_framework import generics
from Common.models import Note
from ..serializers import NoteSerializer


class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all()
        us_id = self.request.query_params.get('us_id') 
        if us_id:
            queryset = queryset.filter(us_id=us_id)
        return queryset

class NoteDetail(generics.ListCreateAPIView):
    serializer_class  = NoteSerializer
    
    def get_queryset(self):
        queryset = Note.objects.all()
        nt_id = self.request.query_params.get('nt_id')
        us_id = self.request.query_params.get('us_id')
        if us_id and nt_id:
            queryset = queryset.filter(us_id=us_id, nt_id=nt_id)
        return queryset