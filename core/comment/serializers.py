from rest_framework import serializers

from .models import Comment


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content']
        read_only_fields = ['author']

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
    # author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['author', 'content', 'date_answered', 'is_correct']
        