from rest_framework import serializers

from .models import Comment
from authentication.serializers import UserProfileSerializer
from home.utils import contains_prohibited_words


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content']
        read_only_fields = ['author']
    
    def validate(self, attrs):
        content = attrs.get('content')
        
        if contains_prohibited_words(content):
            raise serializers.ValidationError('Content contains prohibited words')
        
        return attrs

    def create(self, validated_data):
        post = validated_data.get('post')
        content = validated_data.get('content')
        author = self.context['author']
        return Comment.objects.create(
            post=post, 
            content=content, 
            author=author
        )


class GetPostCommentsSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(many=False)
    date_answered = serializers.SerializerMethodField()
    post_id = serializers.IntegerField(source='post.id')

    class Meta:
        model = Comment
        fields = (
            'id', 
            'author', 
            'post_id', 
            'content', 
            'date_answered',
            'is_correct'
        )

    def get_date_answered(self, obj):
        return int(obj.date_answered.timestamp())
