from rest_framework import serializers
from project.apps.posts.models import Posts
from project.apps.categories.serializers import CategorySerializer, SubcategorySerializer

class PostsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    class Meta:
        model = Posts
        fields = [
            'id',
            'title',
            'slug',
            'body',
            'tags',
            'category',
            'subcategory',    
        ]