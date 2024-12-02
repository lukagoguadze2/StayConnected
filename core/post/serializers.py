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
    title = serializers.CharField()
    description = serializers.CharField()
    likes = serializers.IntegerField(source='like_count')  # must be annotated
    dislikes = serializers.IntegerField(source='dislike_count')  # must be annotated
    comments = serializers.IntegerField(source='comment_count')  # must be annotated
    seen_by_user = serializers.BooleanField()  # must be annotated
    has_correct_answer = serializers.BooleanField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post                         # must be annotated
        fields = ('id', 'author', 'title', 'description',
                  'created_at',
                  'seen_by_user',
                  'likes', 'dislikes', 'comments',
                  'has_correct_answer',
                  'tags')

        read_only_fields = fields

    def get_created_at(self, obj):
        return int(obj.date_posted.timestamp())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['engagement'] = {
            'likes': representation.pop('likes'),
            'dislikes': representation.pop('dislikes'),
            'comments': representation.pop('comments'),
        }
        representation['is_owner'] = self.context['request'].user == instance.author
        representation['has_correct_answer'] = representation.pop('has_correct_answer')
        representation['seen_by_user'] = representation.pop('seen_by_user')
        return representation


class LikePostSerializer(serializers.Serializer):
    reaction_type = serializers.BooleanField()
