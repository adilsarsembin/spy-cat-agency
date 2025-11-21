from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cat
from .serializers import CatSerializer, CatUpdateSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    
    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']:
            return CatUpdateSerializer
        return CatSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
