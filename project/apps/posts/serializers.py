from rest_framework import serializers
from project.apps.posts.models import Posts
from project.apps.categories.models import Category, Subcategory
from project.apps.categories.serializers import CategorySerializer, SubcategorySerializer

class PostsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    slug = serializers.CharField(read_only=True)
    class Meta:
        model = Posts
        fields = [
            'id',
            'title',
            'slug',
            'prev',
            'body',
            'tags',
            'category',
            'subcategory', 
            'created_at'   
        ]