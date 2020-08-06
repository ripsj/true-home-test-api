from rest_framework import serializers
from project.apps.categories.models import Category, Subcategory

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]

class SubcategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subcategory
        fields = [
            'id',
            'name',
            'category',
        ]