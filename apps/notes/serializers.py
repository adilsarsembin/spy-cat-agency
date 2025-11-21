from rest_framework import serializers
from .models import Note
from apps.targets.models import Target
from apps.spy_cats.models import Cat


class NoteSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.name', read_only=True)
    target_name = serializers.CharField(source='target.name', read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'cat', 'target', 'cat_name', 'target_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Note content is required and cannot be empty.")
        return value.strip()
    
    def validate(self, attrs):
        target = attrs.get('target') or self.instance.target if self.instance else None
        
        if target:
            if target.is_completed or target.mission.is_completed:
                raise serializers.ValidationError(
                    "Cannot create or update notes for a completed target or mission. "
                    "Notes are frozen once target or mission is completed."
                )
        
        return attrs


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['target', 'content']
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Note content is required and cannot be empty.")
        return value.strip()
    
    def validate_target(self, value):
        if value.is_completed or value.mission.is_completed:
            raise serializers.ValidationError(
                "Cannot create notes for a completed target or mission."
            )
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            target = validated_data['target']
            if not target.mission.cat:
                raise serializers.ValidationError(
                    "Cannot create note: Mission is not assigned to a cat."
                )
            cat = target.mission.cat
        else:
            target = validated_data['target']
            if not target.mission.cat:
                raise serializers.ValidationError(
                    "Cannot create note: Mission is not assigned to a cat."
                )
            cat = target.mission.cat
        
        validated_data['cat'] = cat
        return super().create(validated_data)


class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['content']
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Note content is required and cannot be empty.")
        return value.strip()
    
    def validate(self, attrs):
        instance = self.instance
        if instance:
            if instance.target.is_completed or instance.target.mission.is_completed:
                raise serializers.ValidationError(
                    "Cannot update notes for a completed target or mission. "
                    "Notes are frozen once target or mission is completed."
                )
        return attrs
