from rest_framework import serializers
from .models import Tag


class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']
    
    def create(self, validated_data):
        title = validated_data.get('title')
        
        if Tag.objects.filter(title=title).exists():
            raise serializers.ValidationError('Tag already exists')
        
        for char in title:
            if not char.isalpha():
                raise serializers.ValidationError(
                    'Title must contain only alphabets'
                )
            
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']
