from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import Response
from project.apps.posts.models import Posts
from project.apps.categories.models import Category, Subcategory
from project.apps.posts.serializers import PostsSerializer

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category__id', 'subcategory__id', 'is_active', 'created_at')
    permission_classes = (permissions.AllowAny, )
    serializer_class = PostsSerializer
    pagination_class = None
    
    def perform_create(self, serializer):
        category = get_object_or_404(Category, pk=self.request.data.get('category'))
        item = serializer.save(
                category=category,
            )
        return Response(item, status=status.HTTP_204_NO_CONTENT)

    # Delete logico
    def destroy(self, request, pk=None):
        posts = get_object_or_404(Posts, pk=pk)
        posts.is_active = False
        posts.save()
        return Response(status=status.HTTP_204_NO_CONTENT)