from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from project.apps.posts.models import Posts
from project.apps.posts.serializers import PostsSerializer

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all().order_by('id')
    serializer_class = PostsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category__id', 'subcategory__id', 'is_active', 'created_at', 'tags')
    permission_classes = (permissions.AllowAny, )