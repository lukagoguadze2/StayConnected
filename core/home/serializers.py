from rest_framework import serializers
from .models import Post, Tag


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']
    
    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')
        post = super().create(validated_data)
        for tag in tags:
            post.tags.add(tag)
        return post
    

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
    

