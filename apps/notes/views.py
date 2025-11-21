from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Note
from .serializers import NoteSerializer, NoteCreateSerializer, NoteUpdateSerializer
from apps.targets.models import Target


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.select_related('cat', 'target').all()
    serializer_class = NoteSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NoteCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NoteUpdateSerializer
        return NoteSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        target_id = self.request.query_params.get('target_id', None)
        
        if target_id:
            queryset = queryset.filter(target_id=target_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        target_id = serializer.validated_data['target'].id
        target = get_object_or_404(Target, pk=target_id)
        
        if not target.mission.cat:
            return Response(
                {"error": "Cannot create note: Mission is not assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if target.is_completed or target.mission.is_completed:
            return Response(
                {"error": "Cannot create notes for a completed target or mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        note = Note.objects.create(
            cat=target.mission.cat,
            target=target,
            content=serializer.validated_data['content']
        )
        
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.target.is_completed or instance.target.mission.is_completed:
            return Response(
                {"error": "Cannot update notes for a completed target or mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
