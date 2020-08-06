from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import Response
from project.apps.categories.models import Category, Subcategory
from project.apps.categories.serializers import CategorySerializer, SubcategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ()
    permission_classes = (permissions.AllowAny, )
    pagination_class = None

    # def perform_create(self, serializer):
    #     item = serializer.save()
    #     return Response(item.data)

    # Soft delete as required
    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.is_active = False
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all().order_by('id')
    serializer_class = SubcategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ()
    permission_classes = (permissions.AllowAny, )
    pagination_class = None

    # Soft delete as required
    def destroy(self, request, pk=None):
        subcategory = get_object_or_404(Subategory, pk=pk)
        subcategory.is_active = False
        subcategory.save()
        return Response(status=status.HTTP_204_NO_CONTENT)