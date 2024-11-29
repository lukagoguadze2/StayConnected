from rest_framework import serializers
from .models import Post, Tag


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']
    
    def create(self, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        tags = validated_data.get('tags')
        post = Post.objects.create(title=title, description=description)
        
        tags = Tag.objects.filter(id__in=tags)
        post.tags.set(tags)
            
        post.save()
        return post
