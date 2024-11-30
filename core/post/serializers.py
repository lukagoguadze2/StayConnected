from rest_framework import serializers
from home.serializers import TagSerializer
from authentication.serializers import UserProfileSerializer
from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'description', 'tags')
        read_only_fields = ('author', )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            post.tags.add(tag)
        post.save()

        return post


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(many=False)
    created_at = serializers.SerializerMethodField()
    seen_by_user = serializers.SerializerMethodField()  # must be annotated
    tags = TagSerializer(many=True)

    class Meta:
        model = Post                         # must be annotated
        fields = ('id', 'author', 'created_at', 'seen_by_user', 'tags')
        read_only_fields = ('author', 'created_at', 'seen_by_user')

    def get_created_at(self, obj):
        return int(obj.date_posted.timestamp())

    def get_seen_by_user(self, obj):
        return obj.seen_by_user  # must be annotated

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_owner'] = self.context['request'].user == instance.author
        return representation


class LikePostSerializer(serializers.Serializer):
    reaction_type = serializers.BooleanField()
