from rest_framework import serializers
from .models import Mission
from apps.targets.models import Target
from apps.spy_cats.models import Cat


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Target name is required and cannot be empty.")
        return value.strip()
    
    def validate_country(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Country is required and cannot be empty.")
        return value.strip()


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['is_completed', 'notes']
    
    def validate(self, attrs):
        instance = self.instance
        if instance:
            if instance.is_completed or instance.mission.is_completed:
                if 'notes' in attrs and attrs['notes'] != instance.notes:
                    raise serializers.ValidationError(
                        "Cannot update notes for a completed target or mission. Notes are frozen once target or mission is completed."
                    )
        return attrs


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=True)
    cat_id = serializers.IntegerField(source='cat.id', read_only=True, allow_null=True)
    
    class Meta:
        model = Mission
        fields = ['id', 'title', 'description', 'cat_id', 'targets', 'is_completed', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Mission title is required and cannot be empty.")
        return value.strip()


class MissionCreateSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Mission
        fields = ['title', 'description', 'cat', 'targets', 'is_completed']
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Mission title is required and cannot be empty.")
        return value.strip()
    
    def validate_targets(self, value):
        if not value:
            raise serializers.ValidationError("At least one target is required.")
        if len(value) < 1:
            raise serializers.ValidationError("A mission must have at least 1 target.")
        if len(value) > 3:
            raise serializers.ValidationError("A mission can have at most 3 targets.")
        
        for target_data in value:
            if not target_data.get('name') or not target_data.get('name', '').strip():
                raise serializers.ValidationError("Each target must have a name.")
            if not target_data.get('country') or not target_data.get('country', '').strip():
                raise serializers.ValidationError("Each target must have a country.")
        
        return value
    
    def validate_cat(self, value):
        if value:
            if hasattr(value, 'mission') and value.mission:
                raise serializers.ValidationError("This cat already has a mission assigned.")
        return value
    
    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        
        return mission


class MissionAssignCatSerializer(serializers.Serializer):
    cat_id = serializers.IntegerField()
    
    def validate_cat_id(self, value):
        try:
            Cat.objects.get(pk=value)
        except Cat.DoesNotExist:
            raise serializers.ValidationError("Cat with this ID does not exist.")
        return value
