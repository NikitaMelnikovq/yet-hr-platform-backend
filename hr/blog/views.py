from django.shortcuts import render
from rest_framework import generics

from blog.serializers import PostSerializer
from blog.models import Post

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()