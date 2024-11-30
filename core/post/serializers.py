from rest_framework import serializers
from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        post = super().create(validated_data)
        for tag in tags:
            post.tags.add(tag)
        return post


class LikePostSerializer(serializers.Serializer):
    reaction_type = serializers.BooleanField()
