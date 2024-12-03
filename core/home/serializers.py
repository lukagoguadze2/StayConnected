import re
from rest_framework import serializers

from .models import Tag
from authentication.models import User
from .utils import contains_prohibited_words


class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']
    
    def create(self, validated_data):
        title = validated_data.get('title')
        
        if Tag.objects.filter(title=title).exists():
            raise serializers.ValidationError('Tag already exists')
        
        if not re.match(r'^[\w\+\-\#]+$', title):
            raise serializers.ValidationError(
                'Title can only contain letters, numbers, and symbols like +, -, #'
            )
        
        if contains_prohibited_words(title):
            raise serializers.ValidationError('Title contains prohibited words')
            
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class LeaderBoardSerializer(serializers.ModelSerializer):
    answered_questions = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'rating', 'answered_questions', 'rank')

    def get_answered_questions(self, obj):
        return self.context.get('answered_questions', 0)

    def get_rank(self, obj):
        return obj.rank


class EmptySerializer(serializers.Serializer):
    pass
