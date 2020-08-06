from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import Response
from project.apps.posts.models import Posts
from project.apps.categories.models import Category, Subcategory
from project.apps.posts.serializers import PostsSerializer
from project.apps.posts.utils import category_and_subcategory_finder, serializer_decider

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category__id', 'subcategory__id', 'is_active', 'created_at')
    permission_classes = (permissions.AllowAny, )
    serializer_class = PostsSerializer
    pagination_class = None
    
    def perform_create(self, serializer):
        category = get_object_or_404(Category, pk=self.request.data.get('category'))
        if Subcategory.objects.filter(pk=self.request.data.get('subcategory')).exists():
            subcategory = Subcategory.objects.get(pk=self.request.data.get('subcategory'))
        else:
            subcategory = None
        item = serializer.save(
                category=category,
                subcategory=subcategory
            )
        return Response(item, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, pk=None):
        posts = get_object_or_404(Posts, pk=pk)
        category, subcategory = category_and_subcategory_finder(self.request.data)        
        serializer = PostsSerializer(
            posts, 
            data=request.data, 
            partial=True
        )        
        if serializer.is_valid():
            data = serializer_decider(serializer, category, subcategory)   
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)        

    # Soft delete as required
    def destroy(self, request, pk=None):
        posts = get_object_or_404(Posts, pk=pk)
        posts.is_active = False
        posts.save()
        return Response(status=status.HTTP_204_NO_CONTENT)