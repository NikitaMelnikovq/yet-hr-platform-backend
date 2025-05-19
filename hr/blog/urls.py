from django.urls import path

from blog.views import PostListView

urlpatterns = [
    path('blog-list/', PostListView.as_view(), name='blog-view'),
]

app_name = 'blog'