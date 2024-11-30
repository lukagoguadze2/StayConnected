from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from .serializers import (
    CreatePostSerializer, 
    CreateTagSerializer,
    TagSerializer,
)

from authentication.serializers import UserProfileSerializer

from .models import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class CreatePostView(CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]


class CreateTagView(CreateAPIView):
    serializer_class = CreateTagSerializer
    permission_classes = [IsAuthenticated]
    

class GetTagsView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Tag.objects.all()
    
    
class LeaderboardView(ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.order_by('-rating')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ranked_users = []
        previous_rating = None
        current_rank = 0

        for index, user in enumerate(queryset, start=1):
            if user.rating != previous_rating:
                current_rank = index
                previous_rating = user.rating

            serialized_user = UserProfileSerializer(user).data
            serialized_user['rank'] = current_rank  # Add the rank directly to the serialized data

            ranked_users.append(serialized_user)

        return Response(ranked_users)
    
        
        