from rest_framework import serializers
from .models import Cat
from .validators import validate_breed


class CatSerializer(serializers.ModelSerializer):
    breed = serializers.CharField(validators=[validate_breed])
    
    class Meta:
        model = Cat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']
        
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required and cannot be empty.")
        return value.strip()
    
    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Years of experience must be a positive number.")
        return value
    
    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be a positive number.")
        return value


class CatUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cat
        fields = ['salary']
        
    def validate(self, attrs):
        for field in ['name', 'years_of_experience', 'breed']:
            if field in attrs:
                raise serializers.ValidationError(
                    f"Cannot update {field}. Only salary can be updated."
                )
        return attrs
