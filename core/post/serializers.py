from rest_framework import serializers
from authentication.serializers import UserProfileSerializer

from .models import Post
from home.serializers import TagSerializer
from home.utils import contains_prohibited_words


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'description', 'tags')
        read_only_fields = ('author', )

    def validate(self, attrs):
        title = attrs.get('title')
        description = attrs.get('description')

        if contains_prohibited_words(title):
            raise serializers.ValidationError('Title contains prohibited words')
        
        if contains_prohibited_words(description):
            raise serializers.ValidationError('Description contains prohibited words')
        
        return attrs
        
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
    engagement = serializers.SerializerMethodField()
    seen_by_user = serializers.BooleanField()  # must be annotated
    has_correct_answer = serializers.BooleanField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post                         # must be annotated
        fields = ('id', 'author', 'title', 'description',
                  'created_at',
                  'seen_by_user',
                  'engagement',
                  'has_correct_answer',
                  'tags')

        read_only_fields = fields

    def get_created_at(self, obj):
        return int(obj.date_posted.timestamp())

    def get_engagement(self, obj) -> dict:
        return {
            'likes': getattr(obj, 'like_count', 0),
            'dislikes': getattr(obj, 'dislike_count', 0),
            'comments': getattr(obj, 'comment_count', 0),
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['is_owner'] = self.context['request'].user == instance.author
        representation['has_correct_answer'] = representation.pop('has_correct_answer')
        representation['seen_by_user'] = representation.pop('seen_by_user')
        return representation


class LikePostSerializer(serializers.Serializer):
    reaction_type = serializers.BooleanField()
