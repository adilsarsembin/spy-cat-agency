from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Mission
from apps.targets.models import Target
from .serializers import (
    MissionSerializer,
    MissionCreateSerializer,
    MissionAssignCatSerializer,
    TargetSerializer,
    TargetUpdateSerializer
)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.prefetch_related('targets').all()
    serializer_class = MissionSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MissionCreateSerializer
        return MissionSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat:
            return Response(
                {"error": "Cannot delete a mission that is assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='assign-cat')
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        serializer = MissionAssignCatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cat_id = serializer.validated_data['cat_id']
        from apps.spy_cats.models import Cat
        
        try:
            cat = Cat.objects.get(pk=cat_id)
        except Cat.DoesNotExist:
            return Response(
                {"error": "Cat with this ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if hasattr(cat, 'mission') and cat.mission:
            return Response(
                {"error": "This cat already has a mission assigned."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if mission.cat:
            return Response(
                {"error": "This mission already has a cat assigned."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        mission.cat = cat
        mission.save()
        
        return Response(MissionSerializer(mission).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get', 'put', 'patch'], url_path='targets/(?P<target_id>[^/.]+)')
    def update_target(self, request, pk=None, target_id=None):
        mission = self.get_object()
        target = get_object_or_404(Target, pk=target_id, mission=mission)
        
        if request.method == 'GET':
            serializer = TargetSerializer(target)
            return Response(serializer.data)
        
        serializer = TargetUpdateSerializer(target, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        mission.check_completion()
        
        return Response(serializer.data)
