from django.conf.urls import url
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from project.apps.categories.views import CategoryViewSet, SubcategoryViewSet

category = CategoryViewSet.as_view({
    'get' : 'list',
    'post' : 'perform_create',
    'put': 'perform_update',
    'patch': 'partial_update',
    'delete': 'perform_destroy'
})

subcategory = SubcategoryViewSet.as_view({
    'get' : 'list',
    'post' : 'perform_create',
    'put': 'perform_update',
    'patch': 'partial_update',
    'delete': 'perform_destroy'
})

urlpatterns = format_suffix_patterns([
    path('category', category, name='categocategoryries'),
    path('subcategory', subcategory, name='subcategory'),
])
