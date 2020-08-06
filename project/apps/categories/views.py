from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from project.apps.categories.models import Category, Subcategory
from project.apps.categories.serializers import CategorySerializer, SubcategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ()
    permission_classes = (permissions.AllowAny, )

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all().order_by('id')
    serializer_class = SubcategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ()
    permission_classes = (permissions.AllowAny, )