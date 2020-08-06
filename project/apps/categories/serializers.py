from rest_framework import serializers
from project.apps.categories.models import Category, Subcategory

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug'
        ]

class SubcategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)    
    class Meta:
        model = Subcategory
        fields = [
            'id',
            'name',
            'category',
            'slug'
        ]