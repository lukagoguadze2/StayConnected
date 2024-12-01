from rest_framework import serializers
from authentication.models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_2'
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_2 = attrs.get('password_2')
        if password != password_2:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        if password and len(password) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long'
            )
        if password and not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                'Password must contain a digit'
            )
        if password and not any(char.isalpha() for char in password):
            raise serializers.ValidationError(
                'Password must contain a letter'
            )
        if password and not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                'Password must contain an uppercase letter'
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_2')
        user = User.objects.create_user(**validated_data)
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    answered_questions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rating', 'answered_questions',)
        
    def get_answered_questions(self, obj):
        return self.context.get('answered_questions', 0)
